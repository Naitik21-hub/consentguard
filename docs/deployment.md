# Deployment

## Vercel (hosted demo)

ConsentGuard runs on Vercel as a Python Function: `vercel_app.py` exposes Streamlit's ASGI app (`st.App`), and `pyproject.toml` (`[tool.vercel] entrypoint`) tells Vercel where it is. Streamlit's browser connection uses WebSockets, which Vercel Functions support in **public beta** (Python ASGI included; checked 2026-10-08).

### Safety default: hosted copies are demo-only
When `VERCEL=1` (set automatically by Vercel), the Live mode option is removed. A public URL with a server-side `ANTHROPIC_API_KEY` would let anyone spend your credits and send personal data through your account, and would contradict the "data stays on your computer" design. To deliberately enable live mode on a deployment, set both `ANTHROPIC_API_KEY` and `CONSENTGUARD_ALLOW_LIVE=1` as Vercel environment variables, and protect the deployment (Vercel Deployment Protection or password) first.

### Known hosted limitations
- **Session resets:** a function can run for at most 300 s on the Hobby plan (800 s on Pro), so the WebSocket closes at that limit. Streamlit reconnects automatically, but the reconnect may reach a different instance, so the current report can be lost. Re-run the demo if that happens.
- **Cold starts:** the first load after a period of inactivity can take several seconds while Streamlit, pandas and pyarrow are imported.
- **Beta:** WebSockets on Vercel are in public beta.
- The `.streamlit/config.toml` `server.address = "localhost"` setting does not apply on Vercel; the deployment is reachable at its public URL according to your Vercel Deployment Protection settings.

### Local test of the same entrypoint
```bash
uvicorn vercel_app:app --port 8000
```

## Streamlit Community Cloud (alternative)
Streamlit's own host keeps a long-lived server process, so sessions do not reset every 5 minutes. Point it at `app.py` in the GitHub repo.
