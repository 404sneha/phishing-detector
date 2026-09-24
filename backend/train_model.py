import pandas as pd
import re
import pickle
import math
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# ---------------- FEATURE FUNCTION ----------------
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


# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/raw/urls.csv")

X = []
y = []

for _, row in df.iterrows():
    try:
        url = str(row["url"])
        label = int(str(row["label"]).strip())

        features = extract_features(url)

        X.append(features)
        y.append(label)

    except:
        continue


# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODEL ----------------
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=0.5,   # 🔥 FIXES BIAS
    eval_metric='logloss'
)

# Train
model.fit(X_train, y_train)

# Accuracy
acc = model.score(X_test, y_test)
print("Accuracy:", acc)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained & saved")
print(df["label"].value_counts())