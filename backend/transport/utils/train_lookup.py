
import pandas as pd
import yaml
import os

def load_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(base_dir, "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_train_databases(config):
    ticket_df = pd.read_csv(config["data"]["full"]["ticket"])
    delay_df  = pd.read_csv(config["data"]["full"]["delay"])
    return ticket_df, delay_df

def lookup_train(train_number: int) -> dict:
    config = load_config()
    ticket_df, delay_df = load_train_databases(config)

    
    ticket_row = ticket_df[ticket_df["Train Number"] == train_number]
    if ticket_row.empty:
        raise ValueError(f"Train {train_number} not found in ticket database")

    
    delay_row = delay_df[delay_df["Train_no"] == train_number]
    if delay_row.empty:
        raise ValueError(f"Train {train_number} not found in delay database")

    # extract first matching row from each
    t = ticket_row.iloc[0]
    d = delay_row.iloc[0]

    
    return {
        "Train_Type":             t["Train Type"],
        "Travel_Distance":        float(t["Travel Distance"]),
        "Number_of_Stations":     int(t["Number of Stations"]),
        "Travel_Time":            float(t["Travel Time"]),
        "Seat_Availability":      str(t["Seat Availability"]),
        "Special_Considerations": str(t["Special Considerations"]),
        "Quota":                  str(t["Quota"]),
        "Distance_Km":            float(d["Distance(Km)"]),
        "Run_frequency":          str(d["Run_frequency"]),
        "Season":                 str(d["Season"]),
        "Train_name":             str(d["Train_name"]),
    }