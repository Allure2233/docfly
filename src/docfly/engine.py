"""Markdown → HTML rendering, directory tree, and front-matter parsing."""

import re
from html import escape
from pathlib import Path
from dataclasses import dataclass, field

import markdown
import frontmatter
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


@dataclass
class Page:
    """One Markdown document."""
    path: Path          # relative to doc root
    title: str
    content_html: str
    order: int = 0

    @property
    def url(self) -> str:
        return "/" + str(self.path.with_suffix("")).replace("\\", "/")


@dataclass
class Section:
    """A folder of pages and sub-sections."""
    name: str
    path: Path
    pages: list[Page] = field(default_factory=list)
    sections: list["Section"] = field(default_factory=list)

    @property
    def url(self) -> str:
        return "/" + str(self.path).replace("\\", "/")


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

_CODE_BLOCK_RE = re.compile(r'<pre><code class="language-(\w+)">([\s\S]*?)</code></pre>')
_FORMATTER = HtmlFormatter(style="monokai", noclasses=True)

_md = markdown.Markdown(
    extensions=[
        "fenced_code",
        "tables",
        "toc",
        "footnotes",
        "attr_list",
        "admonition",
        "nl2br",
        "sane_lists",
    ],
    extension_configs={"toc": {"permalink": " ¶", "permalink_title": "Permalink to this heading"}},
)


def _highlight_block(match: re.Match) -> str:
    lang = match.group(1) or "text"
    code = match.group(2)
    # unescape HTML entities that fenced_code produces
    code = code.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", '"')
    try:
        lexer = get_lexer_by_name(lang, stripall=True)
    except ClassNotFound:
        lexer = TextLexer()
    return highlight(code, lexer, _FORMATTER)


def render_markdown(text: str) -> str:
    """Render Markdown text to HTML with Pygments code highlighting."""
    _md.reset()
    html = _md.convert(text)
    html = _CODE_BLOCK_RE.sub(_highlight_block, html)
    return html


# ---------------------------------------------------------------------------
# Front-matter
# ---------------------------------------------------------------------------

def parse_frontmatter(md_path: Path) -> tuple[str, dict]:
    """Return (body_text, meta_dict) from a Markdown file."""
    with open(md_path, encoding="utf-8") as f:
        post = frontmatter.load(f)
    return post.content or "", dict(post.metadata)


# ---------------------------------------------------------------------------
# Directory tree
# ---------------------------------------------------------------------------

def _index_file(dir_path: Path) -> Path | None:
    """Return index.md or README.md if present, else None."""
    for name in ("index.md", "index.md", "README.md", "readme.md"):
        candidate = dir_path / name
        if candidate.is_file():
            return candidate
    return None


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def build_tree(doc_root: Path) -> Section:
    """Walk doc_root and return the full Section tree."""
    root = Section(name="docs", path=Path("."))

    for entry in sorted(doc_root.rglob("*.md"), key=lambda p: (len(p.parts), str(p))):
        rel = entry.relative_to(doc_root)

        # skip .md files in hidden dirs
        if any(part.startswith(".") for part in rel.parts):
            continue

        # determine parent section in the tree
        parts = list(rel.parts)
        current = root
        for part in parts[:-1]:
            found = None
            for s in current.sections:
                if s.name == part:
                    found = s
                    break
            if found is None:
                found = Section(name=part, path=Path(*parts[: parts.index(part) + 1]))
                current.sections.append(found)
            current = found

        body, meta = parse_frontmatter(entry)
        title = meta.get("title") or entry.stem.replace("-", " ").replace("_", " ").title()
        try:
            order = int(meta.get("order", 0))
        except (TypeError, ValueError):
            order = 0

        current.pages.append(
            Page(path=rel, title=title, content_html=render_markdown(body), order=order)
        )

    # sort pages by order then title
    def sort_section(section: Section):
        section.pages.sort(key=lambda p: (p.order, p.title.lower()))
        for s in section.sections:
            sort_section(s)

    sort_section(root)
    return root


# ---------------------------------------------------------------------------
# Flat page list for "prev / next" navigation
# ---------------------------------------------------------------------------

def flat_pages(section: Section) -> list[Page]:
    result: list[Page] = []
    for page in section.pages:
        result.append(page)
    for s in section.sections:
        result.extend(flat_pages(s))
    return result
