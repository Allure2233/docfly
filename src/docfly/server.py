"""FastAPI server with Jinja2 templates and static files."""

from pathlib import Path
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

from .engine import build_tree, flat_pages

_HERE = Path(__file__).parent
_TEMPLATES_DIR = _HERE.parent.parent / "templates"
_jinja_env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)), auto_reload=True, cache_size=0)

app = FastAPI(title="docfly")

# to be set on serve()
_doc_root: Path = Path(".")
_tree = None


def _render(template_name: str, context: dict) -> HTMLResponse:
    """Render a Jinja2 template, injecting request context."""
    template = _jinja_env.get_template(template_name)
    html = template.render(**context)
    return HTMLResponse(html)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return _render("page.html", {
        "request": request,
        "tree": _tree,
        "page": None,
    })


@app.get("/{path:path}", response_class=HTMLResponse)
async def page(request: Request, path: str):
    all_pages = flat_pages(_tree)
    url = "/" + path
    current = next((p for p in all_pages if p.url == url), None)
    if current is None:
        return _render("page.html", {
            "request": request, "tree": _tree, "page": None, "status_code": 404,
        })

    idx = all_pages.index(current)
    prev_page = all_pages[idx - 1] if idx > 0 else None
    next_page = all_pages[idx + 1] if idx + 1 < len(all_pages) else None

    return _render("page.html", {
        "request": request,
        "tree": _tree,
        "page": current,
        "prev": prev_page,
        "next": next_page,
        "active_url": url,
    })


# ---------------------------------------------------------------------------
# WebSocket for live reload
# ---------------------------------------------------------------------------

_clients: list[WebSocket] = []


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    _clients.append(ws)
    try:
        while True:
            await ws.receive_text()  # keep alive
    except WebSocketDisconnect:
        _clients.remove(ws)


def notify_clients():
    """De-duplicated by caller; inline helper."""
    import asyncio
    loop = asyncio.get_event_loop()
    dead = []
    for ws in _clients:
        try:
            loop.create_task(ws.send_text("reload"))
        except Exception:
            dead.append(ws)
    for ws in dead:
        try:
            _clients.remove(ws)
        except ValueError:
            pass


# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------

static_dir = _HERE.parent.parent / "static"
if static_dir.is_dir():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
