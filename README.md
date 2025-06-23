# 🚀 Enhanced GitHub Pages Blog

A professional blog setup with SEO, RSS, dark mode, and best practices built-in.

## ✨ Features

- **SEO Optimized** - Meta tags, sitemap, RSS feed
- **Dark Mode** - Automatic theme switching
- **Mobile Responsive** - Works perfectly on all devices
- **Frontmatter Support** - Rich post metadata
- **Error Handling** - Robust build process
- **Performance** - Optimized CSS and fast loading
- **Analytics Ready** - Google Analytics integration
- **Social Sharing** - Open Graph and Twitter Cards

## 🛠️ Setup

1. **Fork/Clone** this repository
2. **Update config.py** with your details:
   ```python
   BLOG_TITLE = "Your Blog Name"
   BLOG_AUTHOR = "Your Name"
   BASE_URL = "https://yourusername.github.io/yourrepo"
   ```
3. **Push to GitHub**
4. **Enable Pages**: Settings → Pages → Source → GitHub Actions
5. **Your blog is live!** 🎉

## ✍️ Writing Posts

Create `.md` files in `posts/` with frontmatter:

```yaml
---
title: "Your Post Title"
date: "2024-01-15"
description: "SEO description (150-160 chars)"
tags: ["python", "web", "tutorial"]
---

Your content here...
```

## 🧪 Local Development

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Build site
poetry run python build.py
# Or use the script shortcut:
poetry run build

# View locally
open docs/index.html
```

## 📁 Project Structure

```
├── posts/              # Markdown blog posts
├── templates/          # Jinja2 HTML templates
├── build.py           # Static site generator
├── config.py          # Blog configuration
├── pyproject.toml     # Poetry dependencies & config
├── .github/workflows/ # GitHub Actions
└── docs/             # Generated site (auto-created)
```

## 🎯 Best Practices Included

- **Content**: Frontmatter, proper headings, tags
- **SEO**: Meta tags, sitemap, canonical URLs
- **Performance**: Optimized CSS, fast builds
- **Accessibility**: Semantic HTML, proper contrast
- **Security**: Input validation, safe rendering
- **Mobile**: Responsive design, touch-friendly

## 🔧 Customization

### Styling
Edit CSS in `templates/base.html` - uses CSS custom properties for easy theming.

### Analytics
Uncomment Google Analytics code in `templates/base.html` and add your tracking ID.

### Social Links
Update `config.py` with your social media profiles.

## 📊 Generated Files

- `sitemap.xml` - For search engines
- `feed.xml` - RSS feed for subscribers
- Optimized HTML with proper meta tags
- Mobile-responsive design

## 🚀 Deployment

Every push to `main` triggers:
1. Content validation
2. Site building
3. Build verification
4. Automatic deployment

## 📈 SEO Features

- XML sitemap generation
- RSS feed
- Open Graph meta tags
- Twitter Cards
- Semantic HTML structure
- Mobile-first responsive design
- Fast loading times

Your blog is now ready for professional use! 🎉