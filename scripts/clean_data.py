import pandas as pd
from pathlib import Path

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

df = pd.read_csv("data/raw/support_tickets.csv")

# Dataset overview
print(df.info())
print(df.describe())

# Missing values
print(df.isnull().sum())

# Duplicates
print("Duplicates:", df.duplicated().sum())

# Invalid values
print(df["csat"].value_counts())
print(df["complexity"].value_counts())

# Check resolution time
print(df["resolution_time_min"].describe())

assert df["ticket_id"].is_unique
assert df["csat"].between(1, 5).all()
assert df["quality_score"].between(0, 100).all()
assert (df["resolution_time_min"] > 0).all()

df["date"] = pd.to_datetime(df["date"])

df.to_csv(
    "data/processed/support_tickets_clean.csv",
    index=False
)

print("Data validation completed!")