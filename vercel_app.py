"""ASGI entrypoint for hosting ConsentGuard on Vercel (or any ASGI server).

Vercel imports ``app`` from this module (see [tool.vercel] in pyproject.toml).
Locally you can test the same entrypoint with:  uvicorn vercel_app:app --port 8000

Hosted deployments run in DEMO-ONLY mode unless CONSENTGUARD_ALLOW_LIVE=1 is set,
because a public URL with a server-side API key would let anyone spend your
credits and send personal data through your account. See docs/deployment.md.
"""
from pathlib import Path

import streamlit as st

app = st.App(Path(__file__).resolve().parent / "app.py")
