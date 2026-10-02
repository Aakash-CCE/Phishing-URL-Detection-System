import re
from urllib.parse import urlparse, parse_qs

FEATURE_NAMES = [
    'url_length', 'num_dots', 'num_hyphens', 'num_digits',
    'num_special_chars', 'has_ip_address', 'has_https',
    'num_subdomains', 'has_at_symbol', 'is_shortened',
    'num_params', 'path_length', 'has_suspicious_keywords',
    'domain_length', 'num_slashes', 'has_double_slash_redirect'
]

SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'secure', 'update', 'account', 'signin', 
    'banking', 'paypal', 'confirm'
]

SHORTENING_SERVICES = [
    'bit.ly', 'tinyurl.com', 't.co', 'is.gd', 'goo.gl', 'ow.ly', 'buff.ly'
]

def extract_features(url: str) -> dict:
    """Extract all 16 features from a URL string. Returns dict with feature names as keys."""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    try:
        parsed = urlparse(url)
    except Exception:
        # Fallback if parsing completely fails
        return {f: 0 for f in FEATURE_NAMES}
        
    hostname = parsed.hostname or ''
    path = parsed.path or ''
    query = parsed.query or ''
    scheme = parsed.scheme or ''
    
    # 1. url_length
    url_length = len(url)
    
    # 2. num_dots
    num_dots = url.count('.')
    
    # 3. num_hyphens
    num_hyphens = url.count('-')
    
    # 4. num_digits
    num_digits = sum(c.isdigit() for c in url)
    
    # 5. num_special_chars
    special_chars = set('@!~&%#$^*')
    num_special_chars = sum(1 for c in url if c in special_chars)
    
    # 6. has_ip_address
    ipv4_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    has_ip_address = 1 if re.match(ipv4_pattern, hostname) else 0
    
    # 7. has_https
    has_https = 1 if scheme == 'https' else 0
    
    # 8. num_subdomains
    # A simple estimation: dots in hostname - 1
    num_subdomains = max(0, hostname.count('.') - 1)
    
    # 9. has_at_symbol
    has_at_symbol = 1 if '@' in url else 0
    
    # 10. is_shortened
    is_shortened = 1 if hostname in SHORTENING_SERVICES else 0
    
    # 11. num_params
    if '?' in url:
        num_params = url.count('=')
        if num_params == 0 and len(query) > 0:
            num_params = query.count('&') + 1
    else:
        num_params = 0
        
    # 12. path_length
    path_length = len(path)
    
    # 13. has_suspicious_keywords
    url_lower = url.lower()
    has_suspicious_keywords = 1 if any(kw in url_lower for kw in SUSPICIOUS_KEYWORDS) else 0
    
    # 14. domain_length
    domain_length = len(hostname)
    
    # 15. num_slashes
    num_slashes = url.count('/')
    
    # 16. has_double_slash_redirect
    # Check if '//' appears in the path (after the scheme)
    # The string after '://'
    try:
        rest_of_url = url.split('://', 1)[1]
        has_double_slash_redirect = 1 if '//' in rest_of_url else 0
    except IndexError:
        has_double_slash_redirect = 0

    features = {
        'url_length': url_length,
        'num_dots': num_dots,
        'num_hyphens': num_hyphens,
        'num_digits': num_digits,
        'num_special_chars': num_special_chars,
        'has_ip_address': has_ip_address,
        'has_https': has_https,
        'num_subdomains': num_subdomains,
        'has_at_symbol': has_at_symbol,
        'is_shortened': is_shortened,
        'num_params': num_params,
        'path_length': path_length,
        'has_suspicious_keywords': has_suspicious_keywords,
        'domain_length': domain_length,
        'num_slashes': num_slashes,
        'has_double_slash_redirect': has_double_slash_redirect
    }
    return features

def extract_features_array(url: str) -> list:
    """Extract features as a list in FEATURE_NAMES order."""
    features = extract_features(url)
    return [features[name] for name in FEATURE_NAMES]
