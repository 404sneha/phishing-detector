from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import math
import ssl
import socket
import whois
from urllib.parse import urlparse
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

# ---------------- CACHE ----------------
cache = {}

# ---------------- CONFIG ----------------
FAST_MODE = False  # True = super fast (no WHOIS/SSL)

TRUSTED_DOMAINS = [
    "google.com", "youtube.com", "facebook.com",
    "instagram.com", "amazon.com", "microsoft.com",
    "apple.com", "linkedin.com", "github.com"
]

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return "API is working 🚀"

# ---------------- WHOIS ----------------
def get_domain_age(domain):
    if domain in cache and "age" in cache[domain]:
        return cache[domain]["age"]

    try:
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        age = (datetime.now() - creation_date).days
        cache.setdefault(domain, {})["age"] = age
        return age
    except:
        return -1

# ---------------- SSL ----------------
def get_ssl_valid(domain):
    if domain in cache and "ssl" in cache[domain]:
        return cache[domain]["ssl"]

    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(2)
            s.connect((domain, 443))
            cert = s.getpeercert()

        val = 1 if cert else 0
        cache.setdefault(domain, {})["ssl"] = val
        return val
    except:
        return 0

# ---------------- FEATURE EXTRACTION ----------------
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

    prob = [float(url.count(c)) / len(url) for c in dict.fromkeys(list(url))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    features["entropy"] = entropy

    return list(features.values())

# ---------------- PREDICT ROUTE ----------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"]

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "").lower()

        # ---------------- TRUSTED OVERRIDE ----------------
        if domain in TRUSTED_DOMAINS:
            return jsonify({
                "url": url,
                "result": "Safe (Trusted Domain)",
                "confidence": 0.0,
                "risk_score": 0.0
            })

        # ---------------- ML ----------------
        features = extract_features(url)
        prediction = model.predict([features])[0]
        confidence = model.predict_proba([features])[0][1]

        if math.isnan(confidence):
            confidence = 0.5

        # ---------------- NETWORK CHECKS ----------------
        if FAST_MODE:
            domain_age = 365  # assume safe
            ssl_status = 1
        else:
            domain_age = get_domain_age(domain)
            ssl_status = get_ssl_valid(domain)

        # ---------------- RISK SCORE ----------------
        risk_score = confidence

        if domain_age != -1 and domain_age < 180:
            risk_score += 0.2

        if ssl_status == 0:
            risk_score += 0.2

        risk_score = min(risk_score, 1.0)

        # ---------------- FINAL DECISION ----------------
        if risk_score >= 0.7:
            result = "Phishing"
        elif risk_score <= 0.3:
            result = "Safe"
        else:
            result = "Suspicious"

        return jsonify({
            "url": url,
            "result": result,
            "confidence": round(float(confidence), 3),
            "risk_score": round(float(risk_score), 3),
            "domain_age_days": domain_age,
            "ssl": "Valid" if ssl_status else "No SSL"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)