"""
AUTO AFFILIATE PIPELINE — Daily Article Generator
===================================================
1. Pick a keyword from the topic list
2. Generate SEO-optimized comparison article (you provide via Hermes)
3. Save as HTML page 4. Update index 5. Push to GitHub Pages

Run once daily. Generates 1 article → auto-published on tools-review-blog.
"""
import datetime, json, os, random, re, subprocess, sys
from pathlib import Path

REPO = Path(os.environ.get("HOME", "C:\\Users\\Dhanu")) / "tools-review-blog"
AFFILIATE_FILE = REPO / "affiliates.json"
INDEX_FILE = REPO / "index.html"
ARTICLES_DIR = REPO / "articles"
ARTICLES_DIR.mkdir(exist_ok=True)

# ==================== CONFIG ====================
AFFILIATE_LINKS = {
    "hostinger": "https://hostinger.com?REFERRAL=YOUR_ID",
    "bluehost": "https://bluehost.com/track/YOUR_ID",
    "fiverr": "https://fiverr.com/pe/XXXXX",
    "nordvpn": "https://nordvpn.com?aff_id=XXXXX",
    "getresponse": "https://getresponse.com?REFERRAL=YOUR_ID",
    "shopify": "https://shopify.com/partners/XXXXX",
}

SITE_URL = "https://dhanu1098.github.io/tools-review-blog"

TOPICS = [
    {"title": "Best Web Hosting for Beginners", "keyword": "best web hosting for beginners"},
    {"title": "Hostinger vs Bluehost: Which is Better?", "keyword": "hostinger vs bluehost"},
    {"title": "Best VPN for Streaming in 2026", "keyword": "best vpn for streaming 2026"},
    {"title": "NordVPN Review: Is It Worth It?", "keyword": "nordvpn review"},
    {"title": "Best Email Marketing Tools for Small Business", "keyword": "best email marketing tools"},
    {"title": "GetResponse vs Mailchimp Comparison", "keyword": "getresponse vs mailchimp"},
    {"title": "How to Start an Online Store for Free", "keyword": "start online store free"},
    {"title": "Shopify vs WooCommerce: Honest Comparison", "keyword": "shopify vs woocommerce"},
    {"title": "Best Website Builders for Small Business", "keyword": "best website builders small business"},
    {"title": "Cheap Web Hosting That Doesn't Suck", "keyword": "cheap web hosting good quality"},
    {"title": "Best VPN for Privacy and Security", "keyword": "best vpn for privacy"},
    {"title": "Fiverr vs Upwork: Which is Better for Freelancers?", "keyword": "fiverr vs upwork"},
    {"title": "How to Make Money with Affiliate Marketing", "keyword": "how to start affiliate marketing"},
    {"title": "Best SEO Tools for Bloggers", "keyword": "best seo tools for bloggers"},
    {"title": "Bluehost Review: Pros and Cons", "keyword": "bluehost review pros cons"},
]

USED_TOPICS_FILE = REPO / "used_topics.json"

def load_used_topics():
    if USED_TOPICS_FILE.exists():
        return json.loads(USED_TOPICS_FILE.read_text())
    return []

def save_used_topic(topic_title):
    used = load_used_topics()
    used.append(topic_title)
    USED_TOPICS_FILE.write_text(json.dumps(used, indent=2))

def pick_topic():
    used = load_used_topics()
    available = [t for t in TOPICS if t["title"] not in used]
    if not available:
        used.clear()
        USED_TOPICS_FILE.write_text("[]")
        available = TOPICS
    return random.choice(available)

def create_article_html(topic, content, slug):
    """Wrap article content in HTML template"""
    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    title = topic["title"]
    keyword = topic["keyword"]
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} (2026) | ToolsReview</title>
    <meta name="description" content="Honest {title.lower()} comparison and review. Find the best option for your needs.">
    <meta name="keywords" content="{keyword}, {keyword} 2026, best tools">
    <meta property="og:title" content="{title} (2026) | ToolsReview">
    <meta property="og:description" content="Honest comparison of {keyword}. Find the best option for your needs.">
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0d1117;color:#c9d1d9;line-height:1.8}}
        .container{{max-width:800px;margin:0 auto;padding:20px}}
        nav{{padding:15px;border-bottom:1px solid #21262d;margin-bottom:30px}}
        nav a{{color:#58a6ff;text-decoration:none;font-size:1.1em}}
        h1{{color:#e6edf3;font-size:2em;margin-bottom:10px}}
        .meta{{color:#8b949e;font-size:.9em;margin-bottom:30px;padding-bottom:20px;border-bottom:1px solid #21262d}}
        h2{{color:#58a6ff;font-size:1.4em;margin:30px 0 15px}}
        h3{{color:#c9d1d9;font-size:1.15em;margin:20px 0 10px}}
        p{{margin:15px 0}}
        ul,ol{{margin:15px 0;padding-left:25px}}
        li{{margin:8px 0}}
        .cta{{background:#1f6feb22;border:1px solid #1f6feb44;border-radius:8px;padding:20px;margin:30px 0;text-align:center}}
        .cta a{{display:inline-block;background:#238636;color:#fff;padding:12px 30px;border-radius:6px;text-decoration:none;font-weight:bold;margin:10px}}
        .cta a:hover{{background:#2ea043}}
        .pros-cons{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:20px 0}}
        .pros,.cons{{background:#161b22;border:1px solid #21262d;border-radius:8px;padding:20px}}
        .pros h4{{color:#3fb950;margin-bottom:10px}}
        .cons h4{{color:#f85149;margin-bottom:10px}}
        .verdict{{background:#161b22;border:1px solid #1f6feb44;border-radius:8px;padding:25px;margin:30px 0}}
        .verdict h2{{margin-top:0}}
        table{{width:100%;border-collapse:collapse;margin:20px 0}}
        td,th{{border:1px solid #21262d;padding:12px;text-align:left}}
        th{{background:#161b22}}
        .disclosure{{color:#484f58;font-size:.8em;margin-top:40px;padding:20px;border-top:1px solid #21262d}}
        .disclosure a{{color:#58a6ff}}
    </style>
</head>
<body>
    <nav><div class="container"><a href="{SITE_URL}">← Back to ToolsReview</a></div></nav>
    <div class="container">
        <article>
            <h1>{title} (2026)</h1>
            <p class="meta">Published: {date_str} | ToolsReview Team | {keyword}</p>
            {content}
        </article>
        <p class="disclosure">
            <strong>Disclosure:</strong> Some links in this article are affiliate links. If you click and make a purchase, 
            we may earn a commission at no extra cost to you. This does not affect our recommendations. 
            <a href="{SITE_URL}/disclosure.html">Full disclosure.</a>
        </p>
    </div>
</body>
</html>"""
    return html

def update_index(new_article):
    """Add new article link to index.html"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    
    card_html = f"""
        <article>
            <h2><a href="{SITE_URL}/{new_article['file']}">{new_article['title']}</a></h2>
            <div class="meta">{date_str}</div>
            <p>{new_article['description']}</p>
            <span class="tag">Comparison</span>
            <span class="tag">Review</span>
        </article>"""
    
    # Insert after header, before any existing articles
    marker = "</header>"
    if marker in content:
        content = content.replace(marker, marker + "\n" + card_html)
    
    INDEX_FILE.write_text(content, encoding='utf-8')

def git_push():
    """Commit and push to GitHub"""
    subprocess.run(["git", "add", "."], cwd=REPO, capture_output=True)
    subprocess.run(["git", "commit", "-m", f"New article + index update {datetime.datetime.now().strftime('%Y-%m-%d')}"], 
                   cwd=REPO, capture_output=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=REPO, capture_output=True)
    print("  Pushed to GitHub! Live in ~1 minute at:", SITE_URL)

def pipeline(content_body, description, skip_push=False):
    """Run the full pipeline"""
    topic = pick_topic()
    slug = re.sub(r'[^a-z0-9]+', '-', topic["keyword"].lower()).strip('-')
    filename = f"{slug}.html"
    
    print(f"  Topic: {topic['title']}")
    print(f"  Keyword: {topic['keyword']}")
    print(f"  Slug: {slug}")
    
    article_html = create_article_html(topic, content_body, slug)
    filepath = ARTICLES_DIR / filename
    filepath.write_text(article_html, encoding='utf-8')
    print(f"  Saved: articles/{filename}")
    
    article_info = {
        "title": topic["title"],
        "file": f"articles/{filename}",
        "description": description or f"Honest {topic['title'].lower()} — find the best option for your needs.",
        "date": datetime.datetime.now().isoformat()
    }
    
    update_index(article_info)
    print(f"  Updated index.html")
    
    save_used_topic(topic["title"])
    print(f"  Marked as used")
    
    if not skip_push:
        git_push()
    
    return article_info

if __name__ == "__main__":
    print("=" * 60)
    print("  AFFILIATE BLOG PIPELINE")
    print("=" * 60)
    print()
    print("  This script RUNS the pipeline.")
    print("  Content must be provided by Hermes agent.")
    print()
    print("  Available topics remaining:", len([t for t in TOPICS if t["title"] not in load_used_topics()]))
    print()
    
    topic = pick_topic()
    print(f"  Next topic: {topic['title']}")
    print(f"  Keyword: {topic['keyword']}")
