# Frontend

A single Astro page (static output, no framework runtime) that talks to the FastAPI backend.

```
src/layouts/Base.astro          document shell, Google Fonts (Marcellus, IBM Plex Sans)
src/components/                 Header, Chat (empty state, composer), KnowledgeBase
src/scripts/app.ts              tabs, backend status, chat, source cards, knowledge base view
src/styles/global.css           palette tokens and all component styles (plain CSS, no build plugin)
```

```sh
npm install
npm run dev -- --port 4410     # or just `npm run dev` (Astro default is 4321)
npm run build                  # static site in dist/
```

The backend URL defaults to `http://127.0.0.1:8000`; override it with `PUBLIC_BACKEND_URL` at build/dev time.
The backend allows the origins in its `CORS_ORIGINS` variable (default: `127.0.0.1` and `localhost` on ports 4321 and 4410).

Design notes: the palette follows the League client (navy, gold, hextech teal) as CSS custom properties at the top of
`global.css`. Panels use `clip-path` chamfers instead of any Riot artwork. Animations are disabled under
`prefers-reduced-motion`. Chat history (last 12 messages) lives in `sessionStorage`.
