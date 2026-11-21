
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

# Configuration
N_TICKETS = 20000
N_AGENTS = 50

Path("data/raw").mkdir(parents=True, exist_ok=True)

# 1. Generate agents
teams = ["Payments", "Cards", "Account Support"]
shifts = ["Morning", "Afternoon", "Night"]

agents = pd.DataFrame({
    "agent_id": range(1, N_AGENTS + 1),
    "team": np.random.choice(
        teams, N_AGENTS, p=[0.40, 0.30, 0.30]
    ),
    "experience_months": np.random.randint(
        1, 49, N_AGENTS
    ),
    "shift": np.random.choice(
        shifts, N_AGENTS, p=[0.4, 0.4, 0.2]
    ),
    "employment_type": np.random.choice(
        ["Full-time", "Part-time"],
        N_AGENTS,
        p=[0.8, 0.2]
    )
})

# 2. Generate tickets
tickets = pd.DataFrame({
    "ticket_id": range(1, N_TICKETS + 1),
    "date": np.random.choice(
        pd.date_range("2026-01-01", "2026-06-30"),
        N_TICKETS
    )
})

# Assign team and agent consistently
tickets["team"] = np.random.choice(
    teams, N_TICKETS, p=[0.40, 0.30, 0.30]
)

tickets["agent_id"] = [
    np.random.choice(
        agents.loc[
            agents["team"] == team, "agent_id"
        ].values
    )
    for team in tickets["team"]
]

tickets["channel"] = np.random.choice(
    ["Chat", "Email", "Phone"],
    N_TICKETS,
    p=[0.65, 0.25, 0.10]
)

tickets["issue_type"] = [
    np.random.choice(
        ["Payment", "Card", "Account"],
        p=(
            [0.65, 0.20, 0.15]
            if team == "Payments"
            else [0.15, 0.70, 0.15]
            if team == "Cards"
            else [0.15, 0.15, 0.70]
        )
    )
    for team in tickets["team"]
]

tickets["complexity"] = np.random.choice(
    ["Low", "Medium", "High"],
    N_TICKETS,
    p=[0.45, 0.35, 0.20]
)

# 3. Connect agents with their characteristics
tickets = tickets.merge(
    agents,
    on=["agent_id", "team"],
    how="left"
)

# 4. Generate resolution time
complexity_factor = tickets["complexity"].map({
    "Low": 1.0,
    "Medium": 2.0,
    "High": 3.5
})

team_factor = tickets["team"].map({
    "Payments": 1.30,
    "Cards": 1.00,
    "Account Support": 0.90
})

experience_factor = (
    1 - tickets["experience_months"] * 0.003
).clip(lower=0.80)

shift_factor = tickets["shift"].map({
    "Morning": 1.0,
    "Afternoon": 1.05,
    "Night": 1.20
})

tickets["resolution_time_min"] = (
    np.random.gamma(shape=2, scale=12, size=N_TICKETS)
    * complexity_factor
    * team_factor
    * experience_factor
    * shift_factor
).round(2)

# 5. First Contact Resolution
fcr_probability = (
    0.90
    - 0.12 * (tickets["complexity"] == "Medium")
    - 0.30 * (tickets["complexity"] == "High")
    - 0.10 * (tickets["team"] == "Payments")
    + 0.002 * tickets["experience_months"]
).clip(0.15, 0.97)

tickets["fcr"] = (
    np.random.random(N_TICKETS) < fcr_probability
)

# 6. SLA
sla_target = tickets["complexity"].map({
    "Low": 30,
    "Medium": 60,
    "High": 120
})

tickets["sla_met"] = (
    tickets["resolution_time_min"] <= sla_target
)

# 7. Reopened tickets
reopen_probability = (
    0.04
    + 0.08 * (tickets["complexity"] == "High")
    + 0.05 * (tickets["team"] == "Payments")
    + 0.05 * (~tickets["fcr"])
).clip(0.01, 0.50)

tickets["reopened"] = (
    np.random.random(N_TICKETS) < reopen_probability
)

# 8. Quality score
quality = (
    96
    - 7 * (tickets["complexity"] == "High")
    - 5 * (~tickets["fcr"])
    - 8 * tickets["reopened"]
    - 3 * (tickets["shift"] == "Night")
    + 0.10 * tickets["experience_months"]
    + np.random.normal(0, 4, N_TICKETS)
)

tickets["quality_score"] = quality.clip(0, 100).round(2)

# 9. Customer satisfaction
csat_value = (
    4.7
    - 0.40 * (~tickets["fcr"])
    - 0.45 * tickets["reopened"]
    - 0.30 * (~tickets["sla_met"])
    - 0.15 * (tickets["resolution_time_min"] > 60)
    + np.random.normal(0, 0.45, N_TICKETS)
)

tickets["csat"] = (
    np.rint(csat_value).clip(1, 5).astype(int)
)

# 10. Export
tickets = tickets.drop(columns=[
    "experience_months",
    "shift",
    "employment_type"
])

tickets.to_csv(
    "data/raw/support_tickets.csv", index=False
)

agents.to_csv(
    "data/raw/agents.csv", index=False
)

print("Dataset generated successfully!")
print("Tickets:", len(tickets))
print("Agents:", len(agents))
print(tickets.head())
