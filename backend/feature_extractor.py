import re
import math
from urllib.parse import urlparse

def extract_features(url):
    features = {}

    parsed = urlparse(url)
    domain = parsed.netloc

    features["url_length"] = len(url)
    features["domain_length"] = len(domain)

    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")
    features["num_slashes"] = url.count("/")
    features["num_digits"] = sum(c.isdigit() for c in url)

    features["has_repeated_chars"] = 1 if re.search(r"(.)\1{2,}", url) else 0

    features["has_https"] = 1 if url.startswith("https") else 0
    features["has_ip"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0

    features["subdomain_count"] = domain.count(".")

    suspicious_words = ["login", "secure", "bank", "verify", "account", "update"]
    features["suspicious_words"] = sum(word in url.lower() for word in suspicious_words)

    suspicious_tlds = [".ru", ".tk", ".ml", ".ga", ".cf"]
    features["suspicious_tld"] = 1 if any(url.endswith(tld) for tld in suspicious_tlds) else 0

    # 🔥 NEW FEATURES
    shorteners = ["bit.ly", "tinyurl", "goo.gl"]
    features["is_shortened"] = 1 if any(s in url for s in shorteners) else 0

    features["www_in_middle"] = 1 if "www" in parsed.path else 0
    features["long_url"] = 1 if len(url) > 75 else 0

    # Entropy
    prob = [float(url.count(c)) / len(url) for c in dict.fromkeys(list(url))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    features["entropy"] = entropy

    # 🔥 FIXED ORDER (VERY IMPORTANT)
    return [
        features["url_length"],
        features["domain_length"],
        features["num_dots"],
        features["num_hyphens"],
        features["num_slashes"],
        features["num_digits"],
        features["has_repeated_chars"],
        features["has_https"],
        features["has_ip"],
        features["subdomain_count"],
        features["suspicious_words"],
        features["suspicious_tld"],
        features["is_shortened"],
        features["www_in_middle"],
        features["long_url"],
        features["entropy"]
    ]