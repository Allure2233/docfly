"""CLI entry point — one command to rule them all."""

import argparse
import asyncio
import sys
import webbrowser
from pathlib import Path

import uvicorn
from watchfiles import awatch

from . import server
from .engine import build_tree


def serve(doc_path: str, port: int = 8080, open_browser: bool = False, watch: bool = True):
    """Start the docfly server on `doc_path`."""
    root = Path(doc_path).resolve()
    if not root.is_dir():
        print(f"error: '{doc_path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    server._doc_root = root
    server._tree = build_tree(root)

    config = uvicorn.Config(server.app, host="0.0.0.0", port=port, log_level="warning")
    srv = uvicorn.Server(config)

    async def watcher():
        """Watch for file changes and rebuild tree."""
        async for _ in awatch(root):
            server._tree = build_tree(root)
            server.notify_clients()

    async def main():
        tasks = [asyncio.create_task(srv.serve())]
        if watch:
            tasks.append(asyncio.create_task(watcher()))
        if open_browser:
            webbrowser.open(f"http://localhost:{port}")
        await asyncio.gather(*tasks)

    asyncio.run(main())


def main():
    parser = argparse.ArgumentParser(
        prog="docfly", description="One-command Markdown doc site with live preview."
    )
    parser.add_argument("path", default=".", nargs="?", help="Path to docs directory (default: .)")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Port to listen on (default: 8080)")
    parser.add_argument("--open", "-o", action="store_true", help="Open browser on start")
    parser.add_argument("--no-watch", action="store_true", help="Disable live reload")
    args = parser.parse_args()
    serve(args.path, port=args.port, open_browser=args.open, watch=not args.no_watch)


if __name__ == "__main__":
    main()
