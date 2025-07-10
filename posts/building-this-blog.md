---
title: "Building This Blog: From Zero to GitHub Pages with Python & Poetry"
date: "2025-06-21"
description: "How I built a modern, SEO-optimized blog using Python, Poetry, GitHub Actions, and GitHub Pages - complete with dark mode, theme switching, and RSS feeds."
tags: ["python", "github-pages", "poetry", "blogging", "automation", "seo", "dark-mode"]
---

# Building This Blog: From Zero to GitHub Pages

Welcome to Sam's Log Supplemental! This is the story of how this blog came to life - from conception to deployment in under an hour using modern Python tooling.

## 🎯 The Goal

I wanted a simple, fast blog that could:

- Write posts in Markdown
- Deploy automatically on every push
- Look professional with minimal effort
- Be SEO-friendly out of the box
- Support modern features like dark mode and RSS

## 🛠️ The Tech Stack

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

<h3>🔧 Core Technologies</h3>
<ul>
<li><strong>Python</strong> - Static site generation</li>
<li><strong>Poetry</strong> - Dependency management</li>
<li><strong>Jinja2</strong> - HTML templating</li>
<li><strong>Markdown</strong> - Content writing</li>
<li><strong>GitHub Actions</strong> - CI/CD pipeline</li>
<li><strong>GitHub Pages</strong> - Free hosting</li>
</ul>

</div>
<div>

<h3>📦 Key Dependencies</h3>
<code></code>`toml
[tool.poetry.dependencies]
python = "^3.11"
markdown = "^3.8.2"
jinja2 = "^3.1.2"
python-frontmatter = "^1.0.1"
pytz = "^2023.3"
requests = "^2.32.4"

[tool.poetry.group.dev.dependencies]
black = "^25.0.0"
flake8 = "^7.0.0"
<code></code>`

</div>
</div>

## 🏗️ Architecture Overview

The blog follows a simple static site generator pattern:

1. **Content** - Markdown files with YAML frontmatter
2. **Templates** - Jinja2 HTML templates
3. **Build Script** - Python script that processes everything
4. **Deployment** - GitHub Actions automates the pipeline

```python
def build_site():
    # Setup Markdown with extensions
    md = markdown.Markdown(
        extensions=["meta", "fenced_code", "codehilite", "toc", "tables"]
    )
    
    # Process markdown posts with frontmatter
    posts = []
    for filename in sorted(os.listdir('posts')):
        if filename.endswith('.md'):
            title, date, description, tags, content = extract_metadata(filepath)
            html_content = md.convert(content)
            posts.append({
                'title': title,
                'content': html_content,
                'date': date,
                'description': description,
                'tags': tags,
                'filename': filename.replace('.md', '.html'),
                'url': f"/{filename.replace('.md', '.html')}"
            })
    
    # Copy assets and static files
    shutil.copytree("assets", "docs/assets")
    shutil.copytree("static", "docs/static")
    
    # Generate pages, sitemap, RSS feed
    generate_index(posts)
    generate_sitemap(posts)
    generate_rss(posts)
```

## ✨ Features Implemented

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

<h3>📝 Content Management</h3>
<ul>
<li><strong>Frontmatter support</strong> for metadata</li>
<li><strong>Tag system</strong> for categorization</li>
<li><strong>Automatic date handling</strong></li>
<li><strong>Content validation</strong> in CI</li>
</ul>

<h3>🔍 SEO & Discovery</h3>
<ul>
<li><strong>XML sitemap</strong> generation</li>
<li><strong>RSS feed</strong> for subscribers</li>
<li><strong>Open Graph</strong> meta tags</li>
<li><strong>Twitter Cards</strong> support</li>
<li><strong>Semantic HTML</strong> structure</li>
</ul>

</div>
<div>

<h3>🎨 Design & UX</h3>
<ul>
<li><strong>Multi-theme system</strong> (auto/light/dark/LCARS)</li>
<li><strong>Dynamic banner switching</strong></li>
<li><strong>Local storage</strong> persistence</li>
<li><strong>Mobile-responsive</strong> design</li>
<li><strong>WebP images</strong> optimization</li>
<li><strong>Accessible</strong> markup</li>
</ul>

<h3>👨‍💻 Developer Experience</h3>
<ul>
<li><strong>Poetry</strong> dependency management</li>
<li><strong>GitHub Actions</strong> with caching</li>
<li><strong>Error handling</strong> & validation</li>
<li><strong>Local development</strong> workflow</li>
<li><strong>Code formatting</strong> (Black/Flake8)</li>
</ul>

</div>
</div>

## 🚀 Deployment Pipeline

The GitHub Actions workflow includes advanced features:

```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.13'
    cache: 'pip'

- name: Install Poetry
  uses: snok/install-poetry@v1
  with:
    version: latest
    virtualenvs-create: true
    virtualenvs-in-project: true

- name: Load cached venv
  uses: actions/cache@v4
  with:
    path: .venv
    key: venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('**/poetry.lock') }}

- name: Validate posts
  run: |
    find posts -name "*.md" -exec poetry run python -c "import frontmatter; frontmatter.load(open('{}'))" \;

- name: Build site
  run: poetry run python buildblog.py

- name: Test deployed site
  run: python test_site.py
```

Every push to `main` triggers:

1. Python 3.13 setup with pip caching
2. Poetry installation with virtual environment caching
3. Dependency caching for faster builds
4. Markdown post validation
5. Site building with error handling
6. Build artifact validation
7. Deployment to GitHub Pages
8. Live site testing

## 💡 Key Decisions

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

<h3>🐍 Why Python?</h3>
<ul>
<li>Full build control</li>
<li>Easy customization</li>
<li>Familiar ecosystem</li>
<li>Advanced Markdown processing</li>
</ul>

</div>
<div>

<h3>📦 Why Poetry?</h3>
<ul>
<li>Better dependency resolution</li>
<li>Reproducible builds</li>
<li>Modern packaging</li>
<li>Dev/prod separation</li>
</ul>

</div>
<div>

<h3>🌐 Why GitHub Pages?</h3>
<ul>
<li>Free hosting</li>
<li>Automatic HTTPS/CDN</li>
<li>Actions integration</li>
<li>Custom domains</li>
<li>Artifact management</li>
</ul>

</div>
</div>

## 📊 Performance Results

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

<h3>⚡ Speed</h3>
<ul>
<li><strong>Minimal CSS</strong> - No frameworks</li>
<li><strong>Progressive enhancement</strong></li>
<li><strong>Smart JavaScript</strong></li>
<li><strong>Advanced caching</strong></li>
</ul>

</div>
<div>

<h3>🖼️ Assets</h3>
<ul>
<li><strong>WebP images</strong> - Optimized format</li>
<li><strong>Responsive sizing</strong></li>
<li><strong>CSS variables</strong> - Dynamic theming</li>
<li><strong>External files</strong> - Better caching</li>
</ul>

</div>
<div>

<h3>♿ Accessibility</h3>
<ul>
<li><strong>Semantic HTML5</strong></li>
<li><strong>Proper contrast</strong></li>
<li><strong>Screen reader friendly</strong></li>
<li><strong>Keyboard navigation</strong></li>
</ul>

</div>
</div>

## 🔮 Future Enhancements

Some ideas for future iterations:

- **Search functionality** with client-side indexing
- **Comment system** integration (GitHub Discussions)
- **Analytics dashboard** with privacy-focused tracking
- **Newsletter signup** automation
- **Additional themes** beyond LCARS and Material 3
- **Content management** improvements
- **Performance monitoring** integration

## 🎉 The Result

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

<h3>🎨 Design Features</h3>
<ul>
<li>✅ Multi-theme system</li>
<li>✅ Dynamic banners</li>
<li>✅ Mobile responsive</li>
<li>✅ WebP optimization</li>
</ul>

</div>
<div>

<h3>🔍 SEO & Content</h3>
<ul>
<li>✅ Comprehensive SEO</li>
<li>✅ RSS feed</li>
<li>✅ Content validation</li>
<li>✅ Error handling</li>
</ul>

</div>
<div>

<h3>🚀 DevOps</h3>
<ul>
<li>✅ CI/CD pipeline</li>
<li>✅ Advanced caching</li>
<li>✅ Live site testing</li>
<li>✅ Modern tooling</li>
</ul>

</div>
</div>

The entire setup is maintainable, extensible, and follows current best practices. Most importantly, it gets out of the way and lets me focus on writing.

## 🔗 Resources

- **Repository**: [sam-fakhreddine/thingsBlog](https://github.com/sam-fakhreddine/thingsBlog)
- **Live Site**: [sam-fakhreddine.github.io/thingsBlog](https://sam-fakhreddine.github.io/thingsBlog)
- **Poetry**: [python-poetry.org](https://python-poetry.org)
- **GitHub Pages**: [pages.github.com](https://pages.github.com)
- **GitHub Actions**: [docs.github.com/actions](https://docs.github.com/actions)
- **Markdown Extensions**: [python-markdown.github.io](https://python-markdown.github.io)

---

*This post was written in Markdown, processed by Python, and deployed automatically. The future is pretty cool.* ✨
