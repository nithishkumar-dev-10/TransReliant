import pandas as pd
import yaml

def load_config():
    with open("backend/config.yaml","r") as f:
        return yaml.safe_load(f)
    
def load_lookup_data(config):
    ticket_path=config["data"]["processed"]["ticket"]
    delay_path=config["data"]["processed"]["delay"]

    ticket_df=pd.read_csv(ticket_path)
    delay_df=pd.read_csv(delay_path)

    return ticket_df,delay_df

def lookup_train(train_number: int, ticket_df: pd.DataFrame, delay_df: pd.DataFrame) -> dict:

    ticket_row = ticket_df[ticket_df["Train Number"] == train_number]
    if ticket_row.empty:
        raise ValueError(f"Train {train_number} not found in ticket CSV.")

    delay_row = delay_df[delay_df["Train_no"] == train_number]
    if delay_row.empty:
        raise ValueError(f"Train {train_number} not found in delay CSV.")

    return {
        "ticket": ticket_row.iloc[0].to_dict(),
        "delay":  delay_row.iloc[0].to_dict()
    }
