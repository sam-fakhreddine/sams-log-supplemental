---
title: "Building This Blog: From Zero to GitHub Pages with Python & Poetry"
date: "2025-06-21"
description: "How I built a modern, SEO-optimized blog using Python, Poetry, GitHub Actions, and GitHub Pages - complete with dark mode and RSS feeds."
tags: ["python", "github-pages", "poetry", "blogging", "automation", "seo"]
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
python = "^3.9"
markdown = "^3.5.1"
jinja2 = "^3.1.2"
python-frontmatter = "^1.0.1"
pytz = "^2023.3"
```

## 🏗️ Architecture Overview

The blog follows a simple static site generator pattern:

1. **Content** - Markdown files with YAML frontmatter
2. **Templates** - Jinja2 HTML templates
3. **Build Script** - Python script that processes everything
4. **Deployment** - GitHub Actions automates the pipeline

```python
def build_site():
    # Process markdown posts with frontmatter
    posts = []
    for filename in os.listdir('posts'):
        if filename.endswith('.md'):
            title, date, description, tags, content = extract_metadata(filepath)
            html_content = markdown.convert(content)
            posts.append({
                'title': title,
                'content': html_content,
                'date': date,
                # ... more metadata
            })
    
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

- **Dark mode** with system preference detection
- **Mobile-responsive** design
- **Fast loading** with optimized CSS
- **Accessible** markup and contrast

### Developer Experience

- **Poetry** for dependency management
- **GitHub Actions** for automated deployment
- **Error handling** and build validation
- **Local development** workflow

## 🚀 Deployment Pipeline

The GitHub Actions workflow is beautifully simple:

```yaml
- name: Install Poetry
  uses: snok/install-poetry@v1

- name: Install dependencies
  run: poetry install --only=main

- name: Build site
  run: poetry run python build.py

- name: Deploy to GitHub Pages
  uses: actions/deploy-pages@v2
```

Every push to `main` triggers:

1. Content validation
2. Site building
3. Deployment to GitHub Pages

## 💡 Key Decisions

**Why Python over Jekyll/Hugo?**

- Full control over the build process
- Easy to extend and customize
- Familiar tooling and ecosystem

**Why Poetry over pip?**

- Better dependency resolution
- Lock files for reproducible builds
- Modern Python packaging standards

**Why GitHub Pages?**

- Free hosting
- Automatic HTTPS
- Integrated with GitHub Actions
- Custom domain support

## 📊 Performance Results

The generated site is lightning fast:

- **Minimal CSS** - No frameworks, just custom properties
- **Static HTML** - No JavaScript required
- **Optimized images** - Responsive and properly sized
- **Clean markup** - Semantic and accessible

## 🔮 Future Enhancements

Some ideas for future iterations:

- **Search functionality** with client-side indexing
- **Comment system** integration
- **Analytics dashboard**
- **Newsletter signup** automation
- **Image optimization** pipeline

## 🎉 The Result

In less than an hour, we went from empty directory to fully functional blog with:

- ✅ Professional design with dark mode
- ✅ SEO optimization
- ✅ RSS feed
- ✅ Mobile responsive
- ✅ Automated deployment
- ✅ Modern Python tooling

The entire setup is maintainable, extensible, and follows current best practices. Most importantly, it gets out of the way and lets me focus on writing.

## 🔗 Resources

- **Repository**: [sam-fakhreddine/sams-log-supplemental](https://github.com/sam-fakhreddine/sams-log-supplemental)
- **Live Site**: [sam-fakhreddine.github.io/sams-log-supplemental](https://sam-fakhreddine.github.io/sams-log-supplemental)
- **Poetry**: [python-poetry.org](https://python-poetry.org)
- **GitHub Pages**: [pages.github.com](https://pages.github.com)

---

*This post was written in Markdown, processed by Python, and deployed automatically. The future is pretty cool.* ✨
