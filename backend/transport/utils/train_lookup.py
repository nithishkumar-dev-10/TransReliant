
import pandas as pd
import yaml
import os


def load_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(base_dir, "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def lookup_train(train_number: int) -> dict:
    config    = load_config()
    ticket_df = pd.read_csv(config["data"]["full"]["ticket"])
    ticket_df.columns = ticket_df.columns.str.strip()


    row = ticket_df[ticket_df["Train Number"] == train_number]
    if row.empty:
        raise ValueError(f"Train {train_number} not found in database")

   
    t = row.iloc[0]

    return {
        "Train_Type":             str(t["Train Type"]),
        "Travel_Distance":        float(t["Travel Distance"]),
        "Number_of_Stations":     int(t["Number of Stations"]),
        "Travel_Time":            float(t["Travel Time"]),
        "Seat_Availability":      str(t["Seat Availability"]),
        "Special_Considerations": str(t["Special Considerations"]),
        "Quota":                  str(t["Quota"]),
        "Distance_Km":            float(t["Travel Distance"]),
        "Run_frequency":          "Daily",
    }