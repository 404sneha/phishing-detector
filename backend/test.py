import pandas as pd
import re

df = pd.read_csv("data/raw/urls.csv")

df["url_length"] = df["url"].apply(len)
df["num_dots"] = df["url"].apply(lambda x: x.count("."))
df["num_hyphens"] = df["url"].apply(lambda x: x.count("-"))
df["num_slashes"] = df["url"].apply(lambda x: x.count("/"))
df["num_at"] = df["url"].apply(lambda x: x.count("@"))

df["has_https"] = df["url"].apply(lambda x: 1 if "https" in x else 0)

df["has_ip"] = df["url"].apply(
    lambda x: 1 if re.search(r"\d+\.\d+\.\d+\.\d+", x) else 0
)

suspicious_words = ["login", "secure", "bank", "verify", "account", "update"]

df["suspicious_words"] = df["url"].apply(
    lambda x: sum(word in x.lower() for word in suspicious_words)
)

# SAVE FILE
df.to_csv("data/processed/features.csv", index=False)

print("✅ Features saved")