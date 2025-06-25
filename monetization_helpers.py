#!/usr/bin/env python3
"""
Monetization helper functions for the blog
"""

def amazon_affiliate_link(product_url, associate_tag, link_text="View on Amazon"):
    """
    Generate an Amazon affiliate link
    
    Args:
        product_url (str): The Amazon product URL
        associate_tag (str): Your Amazon Associates tag
        link_text (str): Text to display for the link
    
    Returns:
        str: HTML for the affiliate link
    """
    if not associate_tag:
        return f'<a href="{product_url}" target="_blank" rel="noopener">{link_text}</a>'
    
    # Add associate tag to URL
    separator = "&" if "?" in product_url else "?"
    affiliate_url = f"{product_url}{separator}tag={associate_tag}"
    
    return f'<a href="{affiliate_url}" target="_blank" rel="noopener" class="affiliate-link">{link_text}</a>'

def sponsored_content_block(content, sponsor_name=None):
    """
    Wrap content in a sponsored content block
    
    Args:
        content (str): The sponsored content HTML
        sponsor_name (str): Optional sponsor name
    
    Returns:
        str: HTML for sponsored content block
    """
    sponsor_text = f" - {sponsor_name}" if sponsor_name else ""
    return f'''
    <div class="sponsored-content">
        <div class="sponsor-label">Sponsored Content{sponsor_text}</div>
        {content}
    </div>
    '''

def newsletter_signup_form(action_url="#", button_text="Subscribe"):
    """
    Generate a newsletter signup form
    
    Args:
        action_url (str): Form action URL (e.g., Mailchimp endpoint)
        button_text (str): Button text
    
    Returns:
        str: HTML for newsletter form
    """
    return f'''
    <form class="newsletter-form" action="{action_url}" method="post">
        <input type="email" name="email" placeholder="Your email address" required>
        <button type="submit" class="btn">{button_text}</button>
    </form>
    '''