from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .agent import AgentError, apply_prompt
from .renderer import render_html
from .schema import ChatRequest, ChatResponse, Site
from .storage import create_site, get_site, list_sites

app = FastAPI(title="WebBuilder API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/sites")
def post_site(name: str = "Mijn website") -> Site:
    return create_site(name)


@app.get("/sites")
def get_sites() -> list[Site]:
    return list_sites()


@app.get("/sites/{site_id}")
def get_site_endpoint(site_id: str) -> Site:
    site = get_site(site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="Site niet gevonden")
    return site


@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    site = get_site(request.siteId)
    if site is None:
        raise HTTPException(status_code=404, detail="Site niet gevonden")
    try:
        updated, reply = apply_prompt(site, request.message)
    except AgentError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return ChatResponse(reply=reply, site=updated)


@app.get("/sites/{site_id}/render")
def render(site_id: str) -> HTMLResponse:
    site = get_site(site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="Site niet gevonden")
    return HTMLResponse(render_html(site))
