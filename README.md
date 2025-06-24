# 🚀 Sam's Log Supplemental

A modern, SEO-optimized blog built with Python, Poetry, and GitHub Pages featuring multiple themes and responsive design.

## ✨ Features

- **Multi-Theme Support** - Light, Dark, and LCARS themes with auto-detection
- **SEO Optimized** - Meta tags, sitemap, RSS feed, canonical URLs
- **Mobile Responsive** - 990px desktop width, optimized for all devices
- **External Assets** - Separate CSS and JavaScript files for better caching
- **Frontmatter Support** - Rich post metadata with tags
- **Error Handling** - Robust build process with validation
- **Performance** - Optimized loading with WebP images
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
poetry run python buildblog.py

# Test site
poetry run python test_site.py

# View locally
open docs/index.html
```

## 📁 Project Structure

```
├── posts/              # Markdown blog posts
├── templates/          # Jinja2 HTML templates
│   ├── base.html      # Main template with external JS/CSS
│   ├── index.html     # Homepage template
│   └── post.html      # Individual post template
├── static/            # Static assets
│   ├── styles.css     # Main stylesheet with theme support
│   └── script.js      # Theme switching and banner logic
├── assets/            # Images and media
├── buildblog.py       # Static site generator
├── test_site.py       # Site validation tests
├── config.py          # Blog configuration
├── pyproject.toml     # Poetry dependencies & config
├── .github/workflows/ # GitHub Actions CI/CD
└── docs/             # Generated site (GitHub Pages)
```

## 🎯 Best Practices Included

- **Content**: Frontmatter, proper headings, tags
- **SEO**: Meta tags, sitemap, canonical URLs
- **Performance**: Optimized CSS, fast builds
- **Accessibility**: Semantic HTML, proper contrast
- **Security**: Input validation, safe rendering
- **Mobile**: Responsive design, touch-friendly

## 🔧 Customization

### Themes
Three built-in themes with CSS custom properties:
- **Light** - Clean, professional appearance
- **Dark** - Easy on the eyes for night reading
- **LCARS** - Star Trek inspired retro-futuristic design

### Styling
Edit `static/styles.css` - uses CSS custom properties for easy theming and 990px desktop width.

### JavaScript
Theme switching and banner logic in `static/script.js` with proper DOM ready handling.

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

Every push to `main` triggers GitHub Actions workflow:
1. Poetry dependency installation
2. Site building with `buildblog.py`
3. Site validation with `test_site.py`
4. Automatic deployment to GitHub Pages
5. Tests for CSS, RSS feed, and sitemap availability

## 📈 SEO Features

- XML sitemap generation
- RSS feed
- Open Graph meta tags
- Twitter Cards
- Semantic HTML structure
- Mobile-first responsive design
- Fast loading times

Your blog is now ready for professional use! 🎉