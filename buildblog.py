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
from config import *

def extract_metadata(filepath):
    """Extract metadata from frontmatter or content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        title = post.metadata.get('title', 'Untitled')
        date = post.metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
        description = post.metadata.get('description', '')
        tags = post.metadata.get('tags', [])
        
        # Fallback: extract title from first heading
        if title == 'Untitled' and post.content.strip().startswith('# '):
            title = post.content.split('\n')[0][2:].strip()
        
        return title, date, description, tags, post.content
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return "Error", datetime.now().strftime('%Y-%m-%d'), "", [], ""

def generate_sitemap(posts, base_url=BASE_URL):
    """Generate XML sitemap"""
    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Homepage
    url = ET.SubElement(urlset, 'url')
    ET.SubElement(url, 'loc').text = base_url
    ET.SubElement(url, 'changefreq').text = 'weekly'
    ET.SubElement(url, 'priority').text = '1.0'
    
    # Posts
    for post in posts:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = f"{base_url}/{post['filename']}"
        ET.SubElement(url, 'lastmod').text = post['date']
        ET.SubElement(url, 'changefreq').text = 'monthly'
        ET.SubElement(url, 'priority').text = '0.8'
    
    return ET.tostring(urlset, encoding='unicode')

def generate_rss(posts, base_url=BASE_URL):
    """Generate RSS feed"""
    rss = ET.Element('rss', version="2.0")
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = BLOG_TITLE
    ET.SubElement(channel, 'link').text = base_url
    ET.SubElement(channel, 'description').text = BLOG_DESCRIPTION
    ET.SubElement(channel, 'language').text = 'en-us'
    
    for post in posts[:10]:  # Latest 10 posts
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = post['title']
        ET.SubElement(item, 'link').text = f"{base_url}/{post['filename']}"
        ET.SubElement(item, 'description').text = post.get('description', post['title'])
        ET.SubElement(item, 'pubDate').text = post['date']
        ET.SubElement(item, 'guid').text = f"{base_url}/{post['filename']}"
    
    return ET.tostring(rss, encoding='unicode')

def build_site():
    try:
        # Setup
        env = Environment(loader=FileSystemLoader('templates'))
        md = markdown.Markdown(extensions=['meta', 'fenced_code', 'codehilite', 'toc', 'tables'])
        
        # Create output directory
        os.makedirs('docs', exist_ok=True)
        
        # Copy assets to docs/assets
        if os.path.exists('assets'):
            if os.path.exists('docs/assets'):
                shutil.rmtree('docs/assets')
            shutil.copytree('assets', 'docs/assets')
            print("✅ Copied assets to docs/assets")
        
        # Process posts
        posts = []
        posts_dir = 'posts'
        
        if os.path.exists(posts_dir):
            for filename in sorted(os.listdir(posts_dir)):
                if filename.endswith('.md'):
                    filepath = os.path.join(posts_dir, filename)
                    title, date, description, tags, content = extract_metadata(filepath)
                    
                    if title == "Error":
                        continue
                    
                    html_content = md.convert(content)
                    slug = filename.replace('.md', '.html')
                    
                    post = {
                        'title': title,
                        'date': date,
                        'description': description,
                        'tags': tags,
                        'content': html_content,
                        'filename': slug,
                        'url': f"/{slug}"
                    }
                    posts.append(post)
                    
                    # Generate post page
                    post_template = env.get_template('post.html')
                    post_html = post_template.render(post=post, all_posts=posts, config={'BLOG_TITLE': BLOG_TITLE, 'BLOG_DESCRIPTION': BLOG_DESCRIPTION, 'BLOG_AUTHOR': BLOG_AUTHOR, 'BASE_URL': BASE_URL, 'current_year': datetime.now().year})
                    
                    with open(f'docs/{slug}', 'w', encoding='utf-8') as f:
                        f.write(post_html)
        
        # Sort posts by date (newest first)
        posts.sort(key=lambda x: x['date'], reverse=True)
        
        # Generate index page
        index_template = env.get_template('index.html')
        index_html = index_template.render(posts=posts, config={'BLOG_TITLE': BLOG_TITLE, 'BLOG_DESCRIPTION': BLOG_DESCRIPTION, 'BLOG_AUTHOR': BLOG_AUTHOR, 'BASE_URL': BASE_URL, 'current_year': datetime.now().year})
        
        with open('docs/index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        # Generate sitemap
        sitemap_xml = generate_sitemap(posts)
        with open('docs/sitemap.xml', 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + sitemap_xml)
        
        # Generate RSS feed
        rss_xml = generate_rss(posts)
        with open('docs/feed.xml', 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + rss_xml)
        
        print(f"✅ Built {len(posts)} posts, sitemap, and RSS feed")
        
    except Exception as e:
        print(f"❌ Build failed: {e}")
        raise

if __name__ == '__main__':
    build_site()