import pandas as pd
import sqlite3

conn = sqlite3.connect("data/support.db")

tickets = pd.read_csv(
    "data/processed/support_tickets_clean.csv"
)

agents = pd.read_csv("data/raw/agents.csv")

tickets.to_sql(
    "support_tickets", conn,
    if_exists="replace", index=False
)

agents.to_sql(
    "agents", conn,
    if_exists="replace", index=False
)

conn.close()
