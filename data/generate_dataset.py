"""
generate_dataset.py
-------------------
Generates a synthetic labelled URL dataset for phishing URL detection.
Creates ~3000 URLs across three classes: legitimate, suspicious, phishing.

Usage:
    python data/generate_dataset.py
"""
import csv
import random
import os
import string

random.seed(42)  # Reproducible dataset


def random_string(length=7):
    """Generate a random alphanumeric string."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_legitimate_urls(count=1200):
    """Generate realistic legitimate URLs from well-known domains."""
    urls = []

    domains = [
        "google.com", "github.com", "wikipedia.org", "stackoverflow.com",
        "amazon.com", "microsoft.com", "apple.com", "youtube.com",
        "linkedin.com", "netflix.com", "twitter.com", "facebook.com",
        "reddit.com", "medium.com", "nytimes.com", "bbc.co.uk",
        "cnn.com", "mozilla.org", "python.org", "npmjs.com",
        "docker.com", "aws.amazon.com", "cloud.google.com", "docs.github.com",
        "developer.mozilla.org", "learn.microsoft.com", "education.github.com",
        "maps.google.com", "drive.google.com", "mail.google.com"
    ]

    paths = [
        "", "/", "/about", "/contact", "/help", "/docs", "/blog",
        "/search?q=python", "/user/settings", "/pricing", "/features",
        "/enterprise", "/download", "/support", "/careers", "/privacy",
        "/terms", "/products", "/solutions", "/resources",
        "/en-us/windows", "/dp/B09V3KXJPB", "/wiki/Machine_learning",
        "/questions/tagged/python", "/explore", "/trending",
        "/r/cybersecurity", "/p/article-title-here", "/2024/news-article"
    ]

    for _ in range(count):
        domain = random.choice(domains)
        path = random.choice(paths)
        # 90% use https, 10% use http (some legitimate sites still use http)
        scheme = "https" if random.random() > 0.1 else "http"
        # 70% include www, 30% don't
        www = "www." if random.random() > 0.3 and "." not in domain.split(".")[0] else ""
        urls.append((f"{scheme}://{www}{domain}{path}", "legitimate"))

    return urls


def generate_suspicious_urls(count=800):
    """Generate suspicious URLs - shortened, unusual subdomains, etc."""
    urls = []

    shortener_domains = ["bit.ly", "tinyurl.com", "t.co", "is.gd", "goo.gl", "ow.ly", "buff.ly"]

    for _ in range(count):
        pattern = random.choice(["shortened", "multi_subdomain", "long_params", "uncommon_tld", "numeric_path"])

        if pattern == "shortened":
            # URL shortener links
            domain = random.choice(shortener_domains)
            path = "/" + random_string(random.randint(5, 10))
            scheme = random.choice(["http", "https"])
            urls.append((f"{scheme}://{domain}{path}", "suspicious"))

        elif pattern == "multi_subdomain":
            # Too many subdomains
            sub_count = random.randint(3, 5)
            subs = ".".join(random.choices(["sub1", "test", "dev", "app", "web", "mail", "portal", "cdn", "api"], k=sub_count))
            domain = random.choice(["example.com", "mysite.org", "hosting.net", "server.info"])
            path = "/" + random_string(5)
            urls.append((f"http://{subs}.{domain}{path}", "suspicious"))

        elif pattern == "long_params":
            # Excessive query parameters
            domain = random.choice(["tracker.com", "analytics.net", "redirect.info", "click.org"])
            params = "&".join([f"{random_string(3)}={random_string(8)}" for _ in range(random.randint(4, 8))])
            urls.append((f"http://www.{domain}/page?{params}", "suspicious"))

        elif pattern == "uncommon_tld":
            # Uncommon TLDs
            name = random_string(8)
            tld = random.choice([".xyz", ".top", ".club", ".work", ".buzz", ".icu", ".site"])
            urls.append((f"http://www.{name}{tld}/offer", "suspicious"))

        elif pattern == "numeric_path":
            # Numeric/encoded paths
            domain = random.choice(["redirect.com", "go.info", "link.net"])
            path = "/" + "".join(random.choices(string.digits, k=12))
            urls.append((f"http://{domain}{path}", "suspicious"))

    return urls


def generate_phishing_urls(count=1000):
    """Generate phishing URLs with various attack patterns."""
    urls = []

    suspicious_keywords = ["login", "verify", "secure", "update", "account",
                           "signin", "banking", "paypal", "confirm", "password",
                           "credential", "authenticate", "wallet", "recovery"]

    misspelled_domains = [
        "g00gle.com", "paypall.com", "micros0ft.com", "amaz0n.com",
        "faceb00k.com", "twltter.com", "linkedln.com", "app1e.com",
        "netfliix.com", "gooogle.com", "yahooo.com", "appl3.com",
        "paypa1.com", "mlcrosoft.com", "g0ogle.com", "amazom.com"
    ]

    phishing_domains = [
        "secure-login.com", "account-verify.com", "update-now.net",
        "banking-portal.org", "signin-page.com", "auth-check.info",
        "security-alert.com", "password-reset.net", "credential-update.org",
        "verify-identity.com", "secure-payment.net", "account-recovery.info"
    ]

    for _ in range(count):
        pattern = random.choice([
            "ip_address", "at_symbol", "keyword_stuffed", "hyphen_heavy",
            "misspelled", "double_slash", "long_random", "fake_subdomain",
            "mixed_attack"
        ])

        if pattern == "ip_address":
            # IP address instead of domain
            ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            path = random.choice(["/login.php", "/secure/", "/verify.html",
                                  f"/{random.choice(suspicious_keywords)}.php",
                                  f"/admin/{random_string(5)}"])
            urls.append((f"http://{ip}{path}", "phishing"))

        elif pattern == "at_symbol":
            # @ symbol to disguise actual domain
            legit = random.choice(["google.com", "paypal.com", "microsoft.com", "apple.com"])
            evil = random.choice(phishing_domains)
            path = random.choice(["/login", "/verify", "/account", f"/{random_string(6)}"])
            urls.append((f"http://{legit}@{evil}{path}", "phishing"))

        elif pattern == "keyword_stuffed":
            # Suspicious keywords in domain/path
            kw1 = random.choice(suspicious_keywords)
            kw2 = random.choice(suspicious_keywords)
            domain = random.choice(phishing_domains)
            path = f"/{kw1}/{kw2}?id={random_string(10)}&token={random_string(15)}"
            urls.append((f"http://www.{domain}{path}", "phishing"))

        elif pattern == "hyphen_heavy":
            # Excessive hyphens
            parts = random.choices(suspicious_keywords, k=random.randint(3, 5))
            domain = "-".join(parts) + ".com"
            urls.append((f"http://www.{domain}/login", "phishing"))

        elif pattern == "misspelled":
            # Typosquatting / misspelled domains
            domain = random.choice(misspelled_domains)
            kw = random.choice(suspicious_keywords)
            path = f"/{kw}"
            urls.append((f"https://www.{domain}{path}", "phishing"))

        elif pattern == "double_slash":
            # Double slash redirect trick
            legit = random.choice(["google.com", "microsoft.com", "apple.com"])
            evil = random.choice(phishing_domains)
            urls.append((f"http://www.{legit}//redirect//{evil}/login", "phishing"))

        elif pattern == "long_random":
            # Very long URL with random characters
            domain = random.choice(phishing_domains)
            path = "/" + random_string(40) + "/" + random.choice(suspicious_keywords)
            params = f"?session={random_string(20)}&ref={random_string(15)}&token={random_string(25)}"
            urls.append((f"http://{domain}{path}{params}", "phishing"))

        elif pattern == "fake_subdomain":
            # Legitimate brand as subdomain of phishing domain
            brand = random.choice(["google", "paypal", "microsoft", "apple", "amazon", "netflix"])
            evil_tld = random.choice([".xyz", ".top", ".club", ".icu", ".site", ".info"])
            evil_name = random_string(6)
            kw = random.choice(suspicious_keywords)
            urls.append((f"http://{brand}.{evil_name}{evil_tld}/{kw}", "phishing"))

        elif pattern == "mixed_attack":
            # Combination of multiple suspicious indicators
            ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            kw = random.choice(suspicious_keywords)
            urls.append((f"http://{ip}/{kw}?user={random_string(10)}&redirect=//{random.choice(phishing_domains)}", "phishing"))

    return urls


def main():
    """Generate the full dataset and save as CSV."""
    print("Generating synthetic phishing URL dataset...")

    legitimate = generate_legitimate_urls(1200)
    suspicious = generate_suspicious_urls(800)
    phishing = generate_phishing_urls(1000)

    all_urls = legitimate + suspicious + phishing
    random.shuffle(all_urls)

    # Save to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'dataset.csv')

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'label'])
        writer.writerows(all_urls)

    print(f"Dataset generated successfully!")
    print(f"  Total URLs: {len(all_urls)}")
    print(f"  Legitimate: {len(legitimate)}")
    print(f"  Suspicious: {len(suspicious)}")
    print(f"  Phishing:   {len(phishing)}")
    print(f"  Saved to:   {output_path}")


if __name__ == "__main__":
    main()
