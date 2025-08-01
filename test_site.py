#!/usr/bin/env python3
import requests
import sys
from urllib.parse import urljoin
from config import BASE_URL


def test_site():
    """Test deployed site functionality"""
    errors = []

    # Test main page loads
    try:
        r = requests.get(BASE_URL, timeout=10)
        if r.status_code != 200:
            errors.append(f"Homepage returned {r.status_code}")
        elif "Sam's Log Supplemental" not in r.text:
            errors.append("Homepage missing title")
    except Exception as e:
        errors.append(f"Homepage failed: {e}")

    # Test CSS loads
    try:
        css_url = f"{BASE_URL}/static/styles.css"
        print(f"Testing CSS at {css_url}")
        r = requests.get(css_url, timeout=10)
        if r.status_code != 200:
            errors.append(f"CSS returned {r.status_code}")
        elif "@import" not in r.text:
            errors.append("CSS missing imports")
    except Exception as e:
        errors.append(f"CSS failed: {e}")
        
    # Test base CSS loads
    try:
        base_css_url = f"{BASE_URL}/static/base.css"
        print(f"Testing base CSS at {base_css_url}")
        r = requests.get(base_css_url, timeout=10)
        if r.status_code != 200:
            errors.append(f"Base CSS returned {r.status_code}")
        elif "--primary:" not in r.text:
            errors.append("Base CSS missing theme variables")
    except Exception as e:
        errors.append(f"Base CSS failed: {e}")
        
    # Test theme CSS files
    for theme in ["dark", "lcars", "material3"]:
        try:
            theme_css_url = f"{BASE_URL}/static/themes/{theme}.css"
            print(f"Testing {theme} theme CSS at {theme_css_url}")
            r = requests.get(theme_css_url, timeout=10)
            if r.status_code != 200:
                errors.append(f"{theme} theme CSS returned {r.status_code}")
            elif f"[data-theme=\"{theme}\"]" not in r.text:
                errors.append(f"{theme} theme CSS missing theme selector")
        except Exception as e:
            errors.append(f"{theme} theme CSS failed: {e}")

    # Test feeds
    for feed in ["feed.xml", "sitemap.xml"]:
        try:
            feed_url = f"{BASE_URL}/{feed}"
            print(f"Testing feed at {feed_url}")
            r = requests.get(feed_url, timeout=10)
            if r.status_code != 200:
                errors.append(f"{feed} returned {r.status_code}")
        except Exception as e:
            errors.append(f"{feed} failed: {e}")

    if errors:
        print("❌ Site tests failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ All site tests passed")


if __name__ == "__main__":
    test_site()
