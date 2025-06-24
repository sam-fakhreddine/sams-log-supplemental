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

**Core Technologies:**

- **Python** - Static site generation
- **Poetry** - Modern dependency management
- **Jinja2** - HTML templating
- **Markdown** - Content writing
- **GitHub Actions** - CI/CD pipeline
- **GitHub Pages** - Free hosting

**Key Libraries:**

```toml
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
```

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

### Content Management

- **Frontmatter support** for rich metadata
- **Tag system** for categorization
- **Automatic date handling**
- **Content validation** in CI pipeline

### SEO & Discovery

- **XML sitemap** generation
- **RSS feed** for subscribers
- **Open Graph** meta tags for social sharing
- **Twitter Cards** support
- **Semantic HTML** structure

### Design & UX

- **Advanced theme system** with auto/light/dark modes and LCARS theme
- **Dynamic banner switching** based on selected theme
- **Local storage** theme persistence
- **Mobile-responsive** design with optimized images (WebP format)
- **Fast loading** with optimized CSS and minimal JavaScript
- **Accessible** markup and contrast

### Developer Experience

- **Poetry** for dependency management with dev dependencies
- **GitHub Actions** with advanced caching and validation
- **Comprehensive error handling** and build validation
- **Local development** workflow with live testing
- **Code formatting** with Black and Flake8
- **Post validation** in CI pipeline

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

**Why Python over Jekyll/Hugo?**

- Full control over the build process
- Easy to extend and customize
- Familiar tooling and ecosystem
- Advanced Markdown processing with multiple extensions

**Why Poetry over pip?**

- Better dependency resolution
- Lock files for reproducible builds
- Modern Python packaging standards
- Separate dev dependencies for cleaner production builds

**Why GitHub Pages?**

- Free hosting with excellent uptime
- Automatic HTTPS and CDN
- Integrated with GitHub Actions
- Custom domain support
- Built-in artifact management

## 📊 Performance Results

The generated site is lightning fast:

- **Minimal CSS** - No frameworks, just custom properties with CSS variables
- **Progressive enhancement** - Core functionality works without JavaScript
- **Smart JavaScript** - Theme switching with localStorage persistence
- **Optimized images** - WebP format with responsive sizing
- **Clean markup** - Semantic HTML5 with proper accessibility
- **Advanced caching** - Build-time optimizations and GitHub Actions caching

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

The blog has evolved into a sophisticated static site generator with:

- ✅ Advanced theme system (auto/light/dark/LCARS/Material 3)
- ✅ Dynamic banner switching
- ✅ Comprehensive SEO optimization
- ✅ RSS feed with proper metadata
- ✅ Mobile responsive with WebP images
- ✅ Robust CI/CD pipeline with caching
- ✅ Modern Python tooling with dev dependencies
- ✅ Content validation and error handling
- ✅ Live site testing

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
