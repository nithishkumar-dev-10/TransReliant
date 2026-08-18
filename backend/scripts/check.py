import sys
sys.path.append(".")

import yaml
import pandas as pd

with open("backend/config.yaml", "r") as f:
    config = yaml.safe_load(f)

target = config["features"]["ticket"]["target"]

ticket_df = pd.read_csv(config["data"]["processed"]["ticket"])

print("Target column:", target)
print("\nTarget distribution:")
print(ticket_df[target].value_counts())
print("\nAll columns:")
print(ticket_df.columns.tolist())
