#!/usr/bin/env python3
import os
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import frontmatter
import pytz
import xml.etree.ElementTree as ET
from urllib.parse import quote
from config import (
    BLOG_TITLE, BLOG_DESCRIPTION, BLOG_AUTHOR, BASE_URL, POSTS_PER_PAGE, TIMEZONE,
    DEFAULT_OG_IMAGE, GOOGLE_ANALYTICS_ID, GOOGLE_TAG_MANAGER_ID, SOCIAL_LINKS,
    GOOGLE_ADSENSE_ID, BUY_ME_COFFEE_USERNAME, AMAZON_ASSOCIATE_TAG, ENABLE_NEWSLETTER
)


def extract_metadata(filepath):
    """Extract metadata from frontmatter or content"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        title = post.metadata.get("title", "Untitled")
        date = post.metadata.get("date", datetime.now().strftime("%Y-%m-%d"))
        description = post.metadata.get("description", "")
        tags = post.metadata.get("tags", [])

        # Fallback: extract title from first heading
        if title == "Untitled" and post.content.strip().startswith("# "):
            title = post.content.split("\n")[0][2:].strip()

        return title, date, description, tags, post.content
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return "Error", datetime.now().strftime("%Y-%m-%d"), "", [], ""


def generate_sitemap(posts, base_url=BASE_URL):
    """Generate XML sitemap"""
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Homepage
    url = ET.SubElement(urlset, "url")
    ET.SubElement(url, "loc").text = base_url
    ET.SubElement(url, "changefreq").text = "weekly"
    ET.SubElement(url, "priority").text = "1.0"

    # Posts
    for post in posts:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = f"{base_url}/{post['filename']}"
        ET.SubElement(url, "lastmod").text = post["date"]
        ET.SubElement(url, "changefreq").text = "monthly"
        ET.SubElement(url, "priority").text = "0.8"

    # Format XML with proper indentation
    ET.indent(urlset, space="  ", level=0)
    return ET.tostring(urlset, encoding="unicode")


def generate_robots_txt(base_url=BASE_URL):
    """Generate robots.txt file"""
    return f"""User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml
"""


def generate_rss(posts, base_url=BASE_URL):
    """Generate RSS feed"""
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = BLOG_TITLE
    ET.SubElement(channel, "link").text = base_url
    ET.SubElement(channel, "description").text = BLOG_DESCRIPTION
    ET.SubElement(channel, "language").text = "en-us"

    for post in posts[:10]:  # Latest 10 posts
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = post["title"]
        ET.SubElement(item, "link").text = f"{base_url}/{post['filename']}"
        ET.SubElement(item, "description").text = post.get("description", post["title"])
        ET.SubElement(item, "pubDate").text = post["date"]
        ET.SubElement(item, "guid").text = f"{base_url}/{post['filename']}"

    return ET.tostring(rss, encoding="unicode")


def intersect_filter(a, b):
    """Return the intersection of two lists"""
    return [item for item in a if item in b]

def wordcount_filter(text):
    """Count words in text"""
    import re
    return len(re.findall(r'\b\w+\b', str(text)))

def build_site():
    try:
        # Setup
        env = Environment(loader=FileSystemLoader("templates"))
        env.filters['intersect'] = intersect_filter
        env.filters['wordcount'] = wordcount_filter
        md = markdown.Markdown(
            extensions=["meta", "fenced_code", "codehilite", "toc", "tables"]
        )

        # Create output directory
        os.makedirs("docs", exist_ok=True)

        # Copy assets to docs/assets
        if os.path.exists("assets"):
            if os.path.exists("docs/assets"):
                shutil.rmtree("docs/assets")
            shutil.copytree("assets", "docs/assets")
            print("✅ Copied assets to docs/assets")

        # Copy static files to docs/static
        if os.path.exists("static"):
            if os.path.exists("docs/static"):
                shutil.rmtree("docs/static")
            shutil.copytree("static", "docs/static")
            print("✅ Copied static files to docs/static")

        # Process posts
        posts = []
        posts_dir = "posts"

        if os.path.exists(posts_dir):
            for filename in sorted(os.listdir(posts_dir)):
                if filename.endswith(".md"):
                    filepath = os.path.join(posts_dir, filename)
                    title, date, description, tags, content = extract_metadata(filepath)

                    if title == "Error":
                        continue

                    html_content = md.convert(content)
                    slug = filename.replace(".md", ".html")

                    # Calculate reading time and word count (average reading speed: 200 words per minute)
                    word_count = len(content.split())
                    reading_time = max(1, round(word_count / 200))
                    
                    post = {
                        "title": title,
                        "date": date,
                        "description": description,
                        "tags": tags,
                        "content": html_content,
                        "filename": slug,
                        "url": f"/{slug}",
                        "reading_time": reading_time,
                        "word_count": word_count,
                    }
                    posts.append(post)

                    # Generate post page
                    post_template = env.get_template("post.html")
                    post_html = post_template.render(
                        post=post,
                        all_posts=posts,
                        config={
                            "BLOG_TITLE": BLOG_TITLE,
                            "BLOG_DESCRIPTION": BLOG_DESCRIPTION,
                            "BLOG_AUTHOR": BLOG_AUTHOR,
                            "BASE_URL": BASE_URL,
                            "current_year": datetime.now().year,
                            "GOOGLE_TAG_MANAGER_ID": GOOGLE_TAG_MANAGER_ID,
                            "GOOGLE_ADSENSE_ID": GOOGLE_ADSENSE_ID,
                            "BUY_ME_COFFEE_USERNAME": BUY_ME_COFFEE_USERNAME,
                            "AMAZON_ASSOCIATE_TAG": AMAZON_ASSOCIATE_TAG,
                            "ENABLE_NEWSLETTER": ENABLE_NEWSLETTER,
                        },
                    )

                    with open(f"docs/{slug}", "w", encoding="utf-8") as f:
                        f.write(post_html)

        # Sort posts by date (newest first)
        posts.sort(key=lambda x: x["date"], reverse=True)

        # Generate index page
        index_template = env.get_template("index.html")
        index_html = index_template.render(
            posts=posts,
            config={
                "BLOG_TITLE": BLOG_TITLE,
                "BLOG_DESCRIPTION": BLOG_DESCRIPTION,
                "BLOG_AUTHOR": BLOG_AUTHOR,
                "BASE_URL": BASE_URL,
                "current_year": datetime.now().year,
                "GOOGLE_TAG_MANAGER_ID": GOOGLE_TAG_MANAGER_ID,
                "GOOGLE_ADSENSE_ID": GOOGLE_ADSENSE_ID,
                "BUY_ME_COFFEE_USERNAME": BUY_ME_COFFEE_USERNAME,
                "AMAZON_ASSOCIATE_TAG": AMAZON_ASSOCIATE_TAG,
                "ENABLE_NEWSLETTER": ENABLE_NEWSLETTER,
            },
        )

        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(index_html)

        # Generate 404 page
        error_template = env.get_template("404.html")
        error_html = error_template.render(
            posts=posts,
            config={
                "BLOG_TITLE": BLOG_TITLE,
                "BLOG_DESCRIPTION": BLOG_DESCRIPTION,
                "BLOG_AUTHOR": BLOG_AUTHOR,
                "BASE_URL": BASE_URL,
                "current_year": datetime.now().year,
                "GOOGLE_TAG_MANAGER_ID": GOOGLE_TAG_MANAGER_ID,
                "GOOGLE_ADSENSE_ID": GOOGLE_ADSENSE_ID,
                "BUY_ME_COFFEE_USERNAME": BUY_ME_COFFEE_USERNAME,
                "AMAZON_ASSOCIATE_TAG": AMAZON_ASSOCIATE_TAG,
                "ENABLE_NEWSLETTER": ENABLE_NEWSLETTER,
            },
        )

        with open("docs/404.html", "w", encoding="utf-8") as f:
            f.write(error_html)

        # Generate sitemap
        sitemap_xml = generate_sitemap(posts)
        with open("docs/sitemap.xml", "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + sitemap_xml)

        # Generate robots.txt
        robots_txt = generate_robots_txt()
        with open("docs/robots.txt", "w", encoding="utf-8") as f:
            f.write(robots_txt)

        # Generate RSS feed
        rss_xml = generate_rss(posts)
        with open("docs/feed.xml", "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + rss_xml)

        print(f"✅ Built {len(posts)} posts, sitemap, robots.txt, and RSS feed")

    except Exception as e:
        print(f"❌ Build failed: {e}")
        raise


if __name__ == "__main__":
    build_site()
