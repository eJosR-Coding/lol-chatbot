"""Evaluation harness for the LoL RAG chatbot.

Two question sets, three groups each (in_domain / uncovered / out_of_domain):

* dev      eval/questions.json  used while building retrieval and grounding
* heldout  eval/heldout.json    written before any tuning; only aggregates are
                                inspected while developing

Metrics (retriever alone, at the gate threshold): top-1 accuracy, recall@3, MRR,
correct rejection per group, gate precision. With --e2e every question also goes
through the real /chat endpoint (gate, drift check); the LLM is only called with --llm,
otherwise it is replaced by an unavailable stub so the result is deterministic.

Usage (from the repository root):
    uv run python eval/run_eval.py                  # print the report
    uv run python eval/run_eval.py --e2e [--llm]    # + /chat results
    uv run python eval/run_eval.py --write          # rewrite eval/results.md
    uv run python eval/run_eval.py --json out.json  # per-question JSON report

Text after the line "<!-- manual-notes -->" in eval/results.md is preserved on --write.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import httpx  # noqa: E402

from backend.rag import GATE_THRESHOLD, MODEL_NAME, LolRetriever, load_retriever  # noqa: E402

EVAL = ROOT / "eval"
SETS = {"dev": EVAL / "questions.json", "heldout": EVAL / "heldout.json"}
BASELINE = EVAL / "baseline.json"
RESULTS = EVAL / "results.md"
MARKER = "<!-- manual-notes -->"
GROUPS = ("in_domain", "uncovered", "out_of_domain")
LABELS = {"in_domain": "In KB", "uncovered": "League, not in KB", "out_of_domain": "Out of domain"}
SWEEP = [round(0.30 + 0.05 * i, 2) for i in range(9)]  # 0.30 .. 0.70
RANK_DEPTH = 5


def load_rows(retriever: LolRetriever, path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    by_question = {e.question: e.id for e in retriever.entries}
    rows = []
    for group in GROUPS:
        for item in data[group]:
            res = retriever.retrieve(item["q"], k=RANK_DEPTH)
            expected = [by_question[e] for e in item.get("expected_questions", [])]
            ranked = [c["id"] for c in res["candidates"]]
            rank = next((i + 1 for i, cid in enumerate(ranked) if cid in expected), 0)
            rows.append(
                {
                    "group": group,
                    "q": item["q"],
                    "expected": expected,
                    "top_id": res["id"],
                    "top_term": res["term"],
                    "score": res["score"],
                    "rank": rank,
                }
            )
    return rows


def accepted(row: dict, t: float) -> bool:
    return row["score"] >= t


def correct(row: dict, t: float) -> bool:
    if row["group"] == "in_domain":
        return row["rank"] == 1 and accepted(row, t)
    return not accepted(row, t)


def metrics(rows: list[dict], t: float) -> dict:
    a = [r for r in rows if r["group"] == "in_domain"]
    b = [r for r in rows if r["group"] == "uncovered"]
    c = [r for r in rows if r["group"] == "out_of_domain"]
    passed = [r for r in rows if accepted(r, t)]
    good = sum(r["group"] == "in_domain" and r["rank"] == 1 for r in passed)
    return {
        "top1": sum(r["rank"] == 1 for r in a),
        "recall3": sum(1 <= r["rank"] <= 3 for r in a),
        "mrr": sum(1 / r["rank"] for r in a if r["rank"]) / len(a),
        "accepted_correct": sum(correct(r, t) for r in a),
        "a_n": len(a),
        "rej_b": sum(not accepted(r, t) for r in b),
        "b_n": len(b),
        "rej_c": sum(not accepted(r, t) for r in c),
        "c_n": len(c),
        "gate_precision": (good, len(passed)),
    }


def pct(num: int, den: int) -> str:
    return f"{num}/{den} ({100 * num / den:.0f}%)" if den else "n/a"


def sanity(retriever: LolRetriever) -> int:
    """A verbatim KB question must return its own entry."""
    return sum(retriever.retrieve(e.question)["id"] == e.id for e in retriever.entries)


# --- end to end -------------------------------------------------------------------------


def run_e2e(retriever: LolRetriever, paths: dict[str, Path], use_llm: bool) -> dict[str, list[dict]]:
    from fastapi.testclient import TestClient

    from backend.app import OLLAMA_HOST, create_app

    if use_llm:
        try:
            httpx.get(f"{OLLAMA_HOST}/api/tags", timeout=2).raise_for_status()
        except httpx.HTTPError:
            sys.exit("--llm needs Ollama running (ollama serve) with the model pulled")
        http = httpx.AsyncClient(base_url=OLLAMA_HOST, timeout=120.0)
    else:
        http = httpx.AsyncClient(
            base_url="http://llm.invalid", transport=httpx.MockTransport(lambda _r: httpx.Response(503))
        )
    out: dict[str, list[dict]] = {}
    with TestClient(create_app(retriever=retriever, http=http)) as client:
        for name, path in paths.items():
            data = json.loads(path.read_text(encoding="utf-8"))
            by_question = {e.question: e.id for e in retriever.entries}
            rows = []
            for group in GROUPS:
                for item in data[group]:
                    body = client.post("/chat", json={"message": item["q"], "history": []}).json()
                    expected = [by_question[e] for e in item.get("expected_questions", [])]
                    answered = body["mode"] != "refusal"
                    ok = (answered and body["source_id"] in expected) if group == "in_domain" else not answered
                    rows.append(
                        {"group": group, "q": item["q"], "mode": body["mode"], "reason": body["reason"],
                         "source_id": body["source_id"], "reply": body["reply"], "ok": ok}
                    )
            out[name] = rows
    return out


def e2e_summary(rows: list[dict]) -> dict:
    n = {g: sum(r["group"] == g for r in rows) for g in GROUPS}
    ok = {g: sum(r["group"] == g and r["ok"] for r in rows) for g in GROUPS}
    answered = [r for r in rows if r["mode"] != "refusal"]
    return {
        "ok": ok, "n": n,
        "rewrite": sum(r["mode"] == "rewrite" for r in answered),
        "drift": sum(r["reason"].startswith("drift") for r in answered),
        "no_llm": sum(r["reason"] == "llm_unavailable" for r in answered),
        "answered": len(answered),
    }


# --- rendering --------------------------------------------------------------------------


def md_escape(text: str) -> str:
    return text.replace("|", "\\|")


def before_after(name: str, base: dict, m: dict) -> list[str]:
    def row(label: str, b: tuple[int, int] | None, a: tuple[int, int]) -> str:
        return f"| {label} | {pct(*b) if b else 'n/a'} | {pct(*a)} |"

    b = base[name]
    return [
        "| Metric | v1 (before) | v2 (after) |",
        "|---|---|---|",
        row("In KB: top-1 is the expected entry", (b["in_domain_top1"], b["in_domain_n"]), (m["top1"], m["a_n"])),
        row("In KB: correct and passes the gate", (b["in_domain_accepted_correct"], b["in_domain_n"]), (m["accepted_correct"], m["a_n"])),
        row("In KB: expected entry in top 3", None, (m["recall3"], m["a_n"])),
        f"| In KB: MRR (top {RANK_DEPTH}) | n/a | {m['mrr']:.2f} |",
        row("League, not in KB: refused", (b["uncovered_rejected"], b["uncovered_n"]), (m["rej_b"], m["b_n"])),
        row("Out of domain: refused", (b["out_of_domain_rejected"], b["out_of_domain_n"]), (m["rej_c"], m["c_n"])),
        row("Gate precision: accepted queries with a correct top-1", None, m["gate_precision"]),
    ]


def render(retriever: LolRetriever, data: dict[str, list[dict]], e2e: dict | None, use_llm: bool) -> str:
    t = retriever.threshold
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    out = [
        "# Evaluation results",
        "",
        "Generated by `eval/run_eval.py`. "
        f"Embedding model `{MODEL_NAME}`; KB entries: {len(retriever.entries)}; gate threshold {t}.",
        "",
        "Two question sets with the same three groups: **dev** (30 questions, used while building the "
        "pipeline) and **held-out** (30 questions, committed before any change and inspected only as "
        "aggregates while tuning). Every question is a single turn with no history. "
        "\"Passes the gate\" means the best fused score is at least the gate threshold, which is "
        "when the chatbot answers instead of refusing.",
        "",
        "**v1** is the original pipeline (question-only embeddings, top-1 cosine, gate 0.45 that still "
        "called the LLM); its numbers are in `eval/baseline.json`. **v2** is the current one. "
        f"The gate was chosen on dev only; it is not tuned further on held-out. Sanity check: a verbatim KB "
        f"question returns its own entry for {pct(sanity(retriever), len(retriever.entries))}.",
        "",
    ]
    for name in data:
        m = metrics(data[name], t)
        out += [f"## {name} set: before and after", "", *before_after(name, base, m), ""]
    out += [
        "## Gate sweep (v2)",
        "",
        "The gate is the only knob; this sweep shows what each value would have done. "
        f"The app uses {t}.",
        "",
    ]
    for name in data:
        out += [
            f"**{name}**",
            "",
            "| Gate | In KB correct + accepted | Uncovered refused | Out of domain refused | Gate precision |",
            "|---|---|---|---|---|",
        ]
        for th in SWEEP:
            s = metrics(data[name], th)
            mark = " (app)" if abs(th - t) < 1e-9 else ""
            out.append(
                f"| {th:.2f}{mark} | {pct(s['accepted_correct'], s['a_n'])} | {pct(s['rej_b'], s['b_n'])} | "
                f"{pct(s['rej_c'], s['c_n'])} | {pct(*s['gate_precision'])} |"
            )
        out.append("")
    if e2e:
        llm = "Ollama `qwen2.5:0.5b`" if use_llm else "LLM stubbed as unavailable (deterministic: answers are the KB text)"
        out += [
            "## End to end through `/chat` (v2)",
            "",
            f"Each question goes through the real endpoint: retrieval, gate, then {llm}. "
            "Correct = in-KB questions answered from an expected entry; other groups refused.",
            "",
            "| Set | In KB correct | Uncovered refused | Out of domain refused | Answered: LLM rewrite kept | Answered: fell back to KB text |",
            "|---|---|---|---|---|---|",
        ]
        for name, rows in e2e.items():
            s = e2e_summary(rows)
            fell = s["drift"] + s["no_llm"]
            out.append(
                f"| {name} | {pct(s['ok']['in_domain'], s['n']['in_domain'])} | "
                f"{pct(s['ok']['uncovered'], s['n']['uncovered'])} | {pct(s['ok']['out_of_domain'], s['n']['out_of_domain'])} | "
                f"{s['rewrite']}/{s['answered']} | {fell}/{s['answered']} |"
            )
        out.append("")
        if use_llm:
            out += ["Fallback reasons (answered questions whose rewrite was dropped):", ""]
            for name, rows in e2e.items():
                for r in rows:
                    if r["reason"].startswith("drift"):
                        out.append(f"- {name}: {md_escape(r['q'])} → {r['reason']}")
            out.append("")
    for name in data:
        out += [
            f"## Per-question results: {name} (gate {t})",
            "",
            "| Group | Question | Top entry (#id) | Score | Decision | Correct |",
            "|---|---|---|---|---|---|",
        ]
        for r in data[name]:
            top = f"{md_escape(r['top_term'])} (#{r['top_id']:03d})"
            if r["group"] == "in_domain" and r["rank"] != 1:
                top += " [expected " + ", ".join(f"#{i:03d}" for i in r["expected"]) + "]"
            out.append(
                f"| {LABELS[r['group']]} | {md_escape(r['q'])} | {top} | {r['score']:.3f} | "
                f"{'answers' if accepted(r, t) else 'refuses'} | {'yes' if correct(r, t) else 'NO'} |"
            )
        out.append("")
    out += [MARKER, ""]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true", help="write the report to eval/results.md")
    ap.add_argument("--e2e", action="store_true", help="also run every question through /chat")
    ap.add_argument("--llm", action="store_true", help="with --e2e: call Ollama instead of the stub")
    ap.add_argument("--json", type=Path, help="write the per-question report as JSON")
    args = ap.parse_args()

    retriever = load_retriever()
    data = {name: load_rows(retriever, path) for name, path in SETS.items()}
    e2e = run_e2e(retriever, SETS, args.llm) if args.e2e else None
    report = render(retriever, data, e2e, args.llm)
    print(report)
    if args.json:
        args.json.write_text(
            json.dumps({"gate": retriever.threshold, "retrieval": data, "e2e": e2e}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    if not args.write:
        return
    manual = ""
    if RESULTS.exists() and MARKER in RESULTS.read_text(encoding="utf-8"):
        manual = RESULTS.read_text(encoding="utf-8").split(MARKER, 1)[1]
    report = report.rstrip("\n").removesuffix(MARKER).rstrip("\n") + f"\n\n{MARKER}{manual}"
    RESULTS.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
