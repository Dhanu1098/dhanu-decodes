#!/usr/bin/env python3
"""
BUILD SCRIPT — Dhanu Decodes
Compiles source components and pages into static HTML for GitHub Pages.

Usage:
    python3 build.py          # Build all pages
    python3 build.py --watch  # Watch mode (requires watchdog)

Directory structure:
    src/
      components/
        header.html     → Reusable navbar
        footer.html     → Reusable footer
      pages/
        home.html       → Homepage content (no <body>/<head>)
        articles/
          *.html        → Article page content
        disclosure.html → Disclosure page
      template.html     → Base HTML shell with {{TITLE}}, {{CONTENT}} etc.

    assets/
      css/main.css      → Main stylesheet
      js/main.js        → JavaScript
      images/           → Images & favicon

Output:
    index.html          → Compiled homepage
    articles/*.html     → Compiled articles
    disclosure.html     → Compiled disclosure
"""

import os
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
COMPONENTS = SRC / "components"
PAGES_SRC = SRC / "pages"
TEMPLATE = SRC / "template.html"


def load(path: Path) -> str:
    """Read file content as UTF-8."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_component(name: str) -> str:
    """Load a reusable component (header, footer)."""
    path = COMPONENTS / f"{name}.html"
    if path.exists():
        return load(path)
    print(f"⚠ Warning: Component '{name}' not found at {path}")
    return ""


def load_template() -> str:
    """Load the base HTML template."""
    if TEMPLATE.exists():
        return load(TEMPLATE)

    # Fallback: construct template inline
    header_tpl = load_component("header")
    footer_tpl = load_component("footer")

    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        "<title>{{TITLE}}</title>\n"
        '<meta name="description" content="{{DESCRIPTION}}">\n'
        '<meta property="og:title" content="{{OG_TITLE}}">\n'
        '<meta property="og:description" content="{{OG_DESCRIPTION}}">\n'
        '<link rel="stylesheet" href="/dhanu-decodes/assets/css/main.css">\n'
        '<link rel="icon" type="image/svg+xml" href="/dhanu-decodes/assets/images/favicon.svg">\n'
        "</head>\n<body>\n"
        + header_tpl
        + "\n{{CONTENT}}\n"
        + footer_tpl
        + '\n<button class="scroll-top-btn" aria-label="Scroll to top">&uarr;</button>\n'
        '<script src="/dhanu-decodes/assets/js/main.js"></script>\n'
        "</body>\n</html>"
    )


def render_page(
    content: str,
    title: str,
    description: str = "",
    og_title: str = "",
    og_description: str = "",
) -> str:
    """Populate template placeholders with page data."""
    template = load_template()
    return (
        template.replace("{{CONTENT}}", content)
        .replace("{{TITLE}}", title)
        .replace("{{DESCRIPTION}}", description or title)
        .replace("{{OG_TITLE}}", og_title or title)
        .replace("{{OG_DESCRIPTION}}", og_description or description or title)
    )


def build_home() -> str:
    """Build homepage."""
    content = load(PAGES_SRC / "home.html")
    return render_page(
        content,
        title="Dhanu Decodes — AI Tools Reviews & News",
        description="Honest AI tool reviews, latest AI news, and tutorials. I test AI tools so you don't waste time on bad ones.",
        og_title="Dhanu Decodes — AI Tools Reviews & News",
        og_description="AI tool reviews, news, and honest comparisons by Dhanu. Creator testing AI tools daily.",
    )


def build_article(slug: str, title: str, description: str = "") -> str:
    """Build an article page."""
    src_path = PAGES_SRC / "articles" / f"{slug}.html"
    if not src_path.exists():
        print(f"✗ Article source not found: {src_path}")
        return ""
    content = load(src_path)
    return render_page(
        content,
        title=title,
        description=description or title,
        og_title=title,
        og_description=description or title,
    )


def build_disclosure() -> str:
    """Build disclosure page."""
    src_path = PAGES_SRC / "disclosure.html"
    content = load(src_path) if src_path.exists() else "<h1>Affiliate Disclosure</h1><p>Coming soon.</p>"
    return render_page(
        content,
        title="Affiliate Disclosure | Dhanu Decodes",
        description="How I make money from affiliate links — full transparency.",
    )


def write_output(path: Path, html: str) -> None:
    """Write compiled HTML to output path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {path.relative_to(ROOT)}")


def build_all() -> int:
    """Build all pages. Returns number of failures."""
    failures = 0

    # Page definitions: (path, builder_fn, *args)
    pages = [
        (ROOT / "index.html", build_home),
        (
            ROOT / "articles" / "ai-video-tools.html",
            lambda: build_article(
                "ai-video-tools",
                "Best AI Video Generators in 2026 — Tested by Dhanu | Dhanu Decodes",
                "I tested Runway, Pika, HeyGen, and 4 other AI video tools for making Instagram Reels and YouTube content. Here are the ones that actually worked.",
            ),
        ),
        (
            ROOT / "articles" / "ai-writing-tools.html",
            lambda: build_article(
                "ai-writing-tools",
                "Best AI Writing Tools for Content Creators (2026) | Dhanu Decodes",
                "I tested ChatGPT, Claude, Jasper, and 3 other AI writing tools for daily content creation. Find which one helps write scripts, captions, and blog posts.",
            ),
        ),
        (
            ROOT / "articles" / "ai-image-tools.html",
            lambda: build_article(
                "ai-image-tools",
                "Best AI Image Generators — Coming Soon | Dhanu Decodes",
                "Midjourney vs DALL-E vs Stable Diffusion comparison coming soon.",
            ),
        ),
        (
            ROOT / "articles" / "ai-audio-tools.html",
            lambda: build_article(
                "ai-audio-tools",
                "Best AI Voice & Music Tools — Coming Soon | Dhanu Decodes",
                "AI voice and music tool comparison coming soon.",
            ),
        ),
        (ROOT / "disclosure.html", build_disclosure),
    ]

    print(f"\n🔨 Building Dhanu Decodes...\n")

    for output_path, builder in pages:
        try:
            html = builder()
            if html:
                write_output(output_path, html)
            else:
                failures += 1
        except Exception as e:
            print(f"  ✗ Failed {output_path.name}: {e}")
            failures += 1

    return failures


def watch_mode():
    """Watch for changes and rebuild. Requires watchdog."""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("⚠ watchdog not installed. Install with: pip install watchdog")
        print("Running one-time build instead.\n")
        sys.exit(build_all())

    class RebuildHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path.endswith((".html", ".css", ".js")):
                print(f"\n📝 Detected change: {event.src_path}")
                build_all()

    observer = Observer()
    handler = RebuildHandler()
    observer.schedule(handler, str(SRC), recursive=True)
    observer.schedule(handler, str(ROOT / "assets"), recursive=True)
    observer.start()

    print("👀 Watching for changes... (Ctrl+C to stop)\n")
    build_all()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 Watch mode stopped.")
    observer.join()


def main():
    if "--watch" in sys.argv or "-w" in sys.argv:
        watch_mode()
        return

    failures = build_all()

    if failures:
        print(f"\n❌ Build finished with {failures} failure(s)")
        sys.exit(1)
    else:
        print(f"\n✅ Build complete! Site ready at: {ROOT}")


if __name__ == "__main__":
    main()
