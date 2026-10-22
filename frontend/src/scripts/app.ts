// Client logic: tabs, backend status, chat, knowledge base view.
// Rendering uses plain DOM nodes with classes from styles/global.css.

const BACKEND_URL: string = (import.meta.env.PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
const HISTORY_LIMIT = 12;
const STORAGE_KEY = "lol-glossary-chat-v2";

interface Suggestion { id: number; term: string }
interface ChatReply {
  reply: string;
  mode: "refusal" | "verbatim" | "rewrite";
  reason: string;
  source_id: number | null;
  source_term: string | null;
  matched_question: string;
  matched_answer: string;
  score: number;
  gate: number;
  suggestions: Suggestion[];
}
interface Health { ok: boolean; rewrite: boolean; model: string; llm: boolean | null; entries: number; gate: number }
interface KbEntry { id: number; term: string; question: string; answer: string; aliases: string[]; category: string }
type Turn = { role: "user"; text: string } | { role: "assistant"; text: string; meta: ChatReply };

const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
const log = $<HTMLOListElement>("log");
const empty = $("empty");
const offline = $("offline");
const form = $<HTMLFormElement>("composer");
const input = $<HTMLInputElement>("question");
const sendBtn = $<HTMLButtonElement>("send");
const clearBtn = $<HTMLButtonElement>("clear");
const status = $("status");
const statusText = $("status-text");

let turns: Turn[] = [];
let kb: KbEntry[] = [];
let health: Health | null = null;
let busy = false;

// ---------- small helpers ----------

function el<K extends keyof HTMLElementTagNameMap>(tag: K, className?: string, text?: string): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function normalize(s: string): string {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}

function load(): Turn[] {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as Turn[]) : [];
  } catch {
    return [];
  }
}

function save() {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(turns.slice(-HISTORY_LIMIT * 2)));
  } catch {
    /* storage blocked: the conversation just will not survive a reload */
  }
}

function scrollToEnd() {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  window.scrollTo({ top: document.body.scrollHeight, behavior: reduce ? "auto" : "smooth" });
}

// ---------- status ----------

function setStatus(state: "ok" | "degraded" | "down", text: string) {
  status.dataset.state = state;
  statusText.textContent = text;
}

async function refreshStatus(): Promise<boolean> {
  try {
    const r = await fetch(`${BACKEND_URL}/health`, { signal: AbortSignal.timeout(4000) });
    if (!r.ok) throw new Error(String(r.status));
    health = (await r.json()) as Health;
    if (!health.rewrite) setStatus("ok", "Backend online · rewrite off");
    else if (health.llm) setStatus("ok", `Backend online · rewrite on (experimental) · ${health.model}`);
    else setStatus("degraded", "Backend online · rewrite on, model not running");
    offline.hidden = true;
    $("entry-count").textContent = String(health.entries);
    void ensureKb();
    return true;
  } catch {
    health = null;
    setStatus("down", "Backend offline");
    return false;
  }
}

function showOffline() {
  $("offline-url").textContent = BACKEND_URL;
  offline.hidden = false;
  offline.scrollIntoView({ block: "nearest" });
}

// ---------- rendering ----------

function meter(score: number, gate: number): HTMLElement {
  const wrap = el("span", "meter");
  wrap.setAttribute("aria-hidden", "true");
  const fill = el("span", "meter__fill");
  fill.style.width = `${Math.max(2, Math.min(100, score * 100))}%`;
  const tick = el("i", "meter__gate");
  tick.style.left = `${gate * 100}%`;
  wrap.append(fill, tick);
  return wrap;
}

function howLine(meta: ChatReply): string {
  if (meta.mode === "rewrite")
    return `Experimental rewrite by ${health?.model ?? "the local model"}; kept because it stayed close to the source.`;
  if (meta.reason === "llm_unavailable") return "Glossary text as stored: rewrite is on but the local model is not running.";
  if (/dropped_term|duplicated_word/.test(meta.reason))
    return "Glossary text as stored: the model's rewrite dropped a glossary term or swapped a word, so it was not used.";
  if (meta.reason.startsWith("drift")) return "Glossary text as stored: the model's rewrite drifted from the source, so it was dropped.";
  return "Glossary text as stored. No model rewrote it.";
}

let sourceSeq = 0;

function sourceCard(meta: ChatReply): HTMLElement {
  const id = `source-${++sourceSeq}`;
  const card = el("div", "source");
  const bar = el("div", "source__bar");
  bar.append(
    el("span", "source__meta", `Answer source: entry #${meta.source_id} · ${meta.source_term} · similarity ${meta.score.toFixed(2)}`),
  );
  const toggle = el("button", "link-btn", "Show source") as HTMLButtonElement;
  toggle.type = "button";
  toggle.setAttribute("aria-expanded", "false");
  toggle.setAttribute("aria-controls", id);
  bar.append(toggle);
  const body = el("div", "source__body");
  body.id = id;
  body.hidden = true;
  body.append(el("p", "source__q", meta.matched_question), el("p", "source__a", meta.matched_answer));
  toggle.addEventListener("click", () => {
    const open = body.hidden;
    body.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.textContent = open ? "Hide source" : "Show source";
  });
  card.append(bar, meter(meta.score, meta.gate), el("p", "source__how", howLine(meta)), body);
  return card;
}

function suggestionChips(meta: ChatReply): HTMLElement | null {
  if (!meta.suggestions.length) return null;
  const wrap = el("div", "suggest");
  wrap.append(el("span", "suggest__label", "Closest glossary terms:"));
  const list = el("ul", "chips chips--small");
  for (const s of meta.suggestions) {
    const li = el("li");
    const b = el("button", "chip chamfer", s.term) as HTMLButtonElement;
    b.type = "button";
    b.addEventListener("click", () => ask(kb.find((e) => e.id === s.id)?.question ?? `¿Qué es ${s.term}?`));
    li.append(b);
    list.append(li);
  }
  wrap.append(list);
  return wrap;
}

function renderTurn(turn: Turn): HTMLElement {
  const li = el("li", `turn turn--${turn.role}`);
  if (turn.role === "user") {
    li.append(el("p", "turn__label", "You"), el("p", "bubble", turn.text));
    return li;
  }
  const refused = turn.meta.mode === "refusal";
  li.classList.add(refused ? "turn--refusal" : "turn--answer");
  li.append(el("p", "turn__label", refused ? "Outside the glossary" : "Glossary answer"));
  li.append(el("p", "bubble", turn.text));
  if (refused) {
    const m = turn.meta;
    li.append(
      el("p", "refusal-note", `Closest entry: ${m.matched_question} · similarity ${m.score.toFixed(2)}, below the ${m.gate.toFixed(2)} threshold. No model was called.`),
    );
    const chips = suggestionChips(m);
    if (chips) li.append(chips);
  } else {
    li.append(sourceCard(turn.meta));
  }
  return li;
}

function renderAll() {
  log.replaceChildren(...turns.map(renderTurn));
  empty.hidden = turns.length > 0;
  clearBtn.hidden = turns.length === 0;
}

function showPending(): HTMLElement {
  const li = el("li", "turn turn--assistant turn--pending");
  const p = el("p", "bubble bubble--pending");
  p.append(el("span", "", "Looking it up in the glossary"), el("span", "dots"));
  li.append(el("p", "turn__label", "Glossary answer"), p);
  log.append(li);
  scrollToEnd();
  return li;
}

// ---------- chat ----------

async function ask(question: string) {
  const text = question.trim();
  if (!text || busy) return;
  busy = true;
  sendBtn.disabled = true;
  input.value = "";
  const history = turns.slice(-HISTORY_LIMIT).map((t) => ({ role: t.role, content: t.text }));
  turns.push({ role: "user", text });
  renderAll();
  const pending = showPending();
  try {
    const r = await fetch(`${BACKEND_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history }),
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const meta = (await r.json()) as ChatReply;
    turns.push({ role: "assistant", text: meta.reply, meta });
    pending.remove();
    save();
    renderAll();
    offline.hidden = true;
  } catch {
    pending.remove();
    turns.pop(); // the question was not answered: drop it so history stays consistent
    renderAll();
    input.value = text;
    await refreshStatus();
    showOffline();
  } finally {
    busy = false;
    sendBtn.disabled = false;
    input.focus();
    scrollToEnd();
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  void ask(input.value);
});
document.querySelectorAll<HTMLButtonElement>("[data-example]").forEach((b) =>
  b.addEventListener("click", () => void ask(b.dataset.example ?? "")),
);
clearBtn.addEventListener("click", () => {
  turns = [];
  save();
  renderAll();
  input.focus();
});
$("retry").addEventListener("click", async () => {
  if (await refreshStatus()) input.focus();
  else showOffline();
});

// ---------- tabs ----------

const tabs = Array.from(document.querySelectorAll<HTMLButtonElement>(".tab"));

function selectView(view: "chat" | "kb", focus = false) {
  for (const t of tabs) {
    const on = t.dataset.view === view;
    t.setAttribute("aria-selected", String(on));
    t.tabIndex = on ? 0 : -1;
    if (on && focus) t.focus();
  }
  $("view-chat").hidden = view !== "chat";
  $("view-kb").hidden = view !== "kb";
  form.hidden = view !== "chat";
  if (view === "kb") void ensureKb();
  else input.focus({ preventScroll: true });
}

tabs.forEach((t, i) => {
  t.addEventListener("click", () => selectView(t.dataset.view as "chat" | "kb"));
  t.addEventListener("keydown", (e) => {
    if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
    const next = tabs[(i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length];
    selectView(next.dataset.view as "chat" | "kb", true);
  });
});

// ---------- knowledge base ----------

const kbList = $<HTMLUListElement>("kb-list");
const kbSearch = $<HTMLInputElement>("kb-search");
const kbCategory = $<HTMLSelectElement>("kb-category");
const kbCount = $("kb-count");
const kbEmpty = $("kb-empty");

const CATEGORY_LABEL: Record<string, string> = {
  game_mode: "Game modes",
  role: "Roles",
  crowd_control: "Crowd control",
  stat: "Stats",
  map: "Map and objectives",
  chat: "Chat slang",
  tactic: "Tactics",
  mechanics: "Mechanics",
};

async function ensureKb() {
  if (kb.length) return;
  try {
    const r = await fetch(`${BACKEND_URL}/kb`);
    if (!r.ok) throw new Error(String(r.status));
    kb = ((await r.json()) as { entries: KbEntry[] }).entries;
    const cats = [...new Set(kb.map((e) => e.category))].sort();
    for (const c of cats) kbCategory.append(new Option(CATEGORY_LABEL[c] ?? c, c));
    renderKb();
  } catch {
    kbCount.textContent = "The knowledge base could not be loaded: the backend is offline.";
  }
}

function kbCard(e: KbEntry): HTMLElement {
  const li = el("li", "kb-card");
  const head = el("div", "kb-card__head");
  head.append(el("span", "kb-card__id", `#${String(e.id).padStart(3, "0")}`), el("h3", "kb-card__term", e.term));
  li.append(head, el("p", "kb-card__answer", e.answer));
  const foot = el("div", "kb-card__foot");
  foot.append(el("span", "tag tag--category", CATEGORY_LABEL[e.category] ?? e.category));
  for (const a of e.aliases.slice(0, 4)) foot.append(el("span", "tag", a));
  li.append(foot);
  return li;
}

function renderKb() {
  const q = normalize(kbSearch.value.trim());
  const cat = kbCategory.value;
  const shown = kb.filter(
    (e) =>
      (!cat || e.category === cat) &&
      (!q || normalize([e.term, e.question, e.answer, ...e.aliases].join(" ")).includes(q)),
  );
  kbList.replaceChildren(...shown.map(kbCard));
  kbEmpty.hidden = shown.length > 0;
  kbCount.textContent = `${shown.length} of ${kb.length} entries`;
}

kbSearch.addEventListener("input", renderKb);
kbCategory.addEventListener("change", renderKb);

// ---------- start ----------

turns = load();
renderAll();
void refreshStatus().then((ok) => {
  if (!ok && turns.length === 0) showOffline();
});
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) void refreshStatus();
});
setInterval(() => {
  if (!document.hidden) void refreshStatus();
}, 30000);
input.focus({ preventScroll: true });
