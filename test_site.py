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
        css_url = urljoin(BASE_URL, "/static/styles.css")
        r = requests.get(css_url, timeout=10)
        if r.status_code != 200:
            errors.append(f"CSS returned {r.status_code}")
        elif "--primary:" not in r.text:
            errors.append("CSS missing theme variables")
    except Exception as e:
        errors.append(f"CSS failed: {e}")
    
    # Test feeds
    for feed in ["/feed.xml", "/sitemap.xml"]:
        try:
            r = requests.get(urljoin(BASE_URL, feed), timeout=10)
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