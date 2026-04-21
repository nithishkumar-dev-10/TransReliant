"""importing the required libraries and modules """

import pandas as pd
import yaml
import os


"""defining the function to build the data for training and testing the model"""


#loading the config file

def load_config():
    with open("backend/config.yaml", "r") as f:
        return yaml.safe_load(f)
    


# loading the data based on the specified mode in the config file

def load_data(config):
    mode = config["mode"]

    if mode == "full":
        ticket_path = config["data"]["full"]["ticket"]
        delay_path  = config["data"]["full"]["delay"]

    elif mode == "sample":
        ticket_path = config["data"]["sample"]["ticket"]
        delay_path  = config["data"]["sample"]["delay"]

    else:
        raise ValueError(f"Invalid mode: {mode}. Use 'full' or 'sample'")

    ticket_df = pd.read_csv(ticket_path)
    delay_df  = pd.read_csv(delay_path)

    print(f"Mode     : {mode}")
    print(f"Ticket   : {ticket_df.shape}")
    print(f"Delay    : {delay_df.shape}")

    return ticket_df, delay_df



# cleaning the ticket_confirmation data

def clean_ticket(df, config):
    # strip whitespace from column names
    df.columns = df.columns.str.strip()

    # drop rows with missing values FIRST
    df = df.dropna()

    # convert target column to binary BEFORE dropping anything
    df["Confirmation Status"] = df["Confirmation Status"].map(
        {"Confirmed": 1, "Not Confirmed": 0}
    )
    df = df.dropna(subset=["Confirmation Status"])

    # extract features from Date of Journey BEFORE dropping it
    df["Date of Journey"] = pd.to_datetime(
        df["Date of Journey"], errors="coerce"
    )
    df["journey_month"]     = df["Date of Journey"].dt.month
    df["journey_dayofweek"] = df["Date of Journey"].dt.dayofweek

    # extract days before journey BEFORE dropping Booking Date
    df["Booking Date"] = pd.to_datetime(
        df["Booking Date"], errors="coerce"
    )
    df["days_before_journey"] = (
        df["Date of Journey"] - df["Booking Date"]
    ).dt.days

    # NOW drop useless columns after extracting what we need
    drop_cols = config["features"]["ticket"]["drop"]
    df = df.drop(columns=drop_cols, errors="ignore")
    df = df.drop(columns=["Date of Journey", "Booking Date"], errors="ignore")

    print(f"Ticket cleaned: {df.shape}")
    return df

# cleaning the delay data 

def clean_delay(df, config):
    # fix typos in column names from raw data
    df = df.rename(columns={
        "Dealy_min":    "Delay_min",
        "Destitnation": "Destination"
    })

    # strip whitespace from column names
    df.columns = df.columns.str.strip()

    # drop useless columns
    drop_cols = config["features"]["delay"]["drop"]
    df = df.drop(columns=drop_cols, errors="ignore")

    # drop rows with missing values
    df = df.dropna()

    # convert delay from HH:MM:SS string to total minutes as integer
    def to_minutes(t):
        try:
            parts = str(t).strip().split(":")
            h = int(parts[0])
            m = int(parts[1])
            return h * 60 + m
        except:
            return None

    df["Delay_min"] = df["Delay_min"].apply(to_minutes)

    # drop rows where delay conversion failed
    df = df.dropna(subset=["Delay_min"])

    # convert delay to float
    df["Delay_min"] = df["Delay_min"].astype(float)

    # convert date to month and day of week
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["journey_month"]     = df["Date"].dt.month
    df["journey_dayofweek"] = df["Date"].dt.dayofweek
    df = df.drop(columns=["Date"])

    print(f"Delay cleaned: {df.shape}")
    return df

# saving the cleaned data into the processed folder

def save_processed(ticket_df, delay_df, config):
    ticket_out = config["data"]["processed"]["ticket"]
    delay_out  = config["data"]["processed"]["delay"]

    os.makedirs("backend/data/processed", exist_ok=True)

    ticket_df.to_csv(ticket_out, index=False)
    delay_df.to_csv(delay_out,   index=False)

    print(f"Saved → {ticket_out}")
    print(f"Saved → {delay_out}")

# creating the main function to call the defined functions in a proper order

if __name__ == "__main__":
    config = load_config()

    ticket_df, delay_df = load_data(config)

    ticket_df = clean_ticket(ticket_df, config)
    delay_df  = clean_delay(delay_df,  config)

    save_processed(ticket_df, delay_df, config)

    print("\n--- Ticket Sample ---")
    print(ticket_df.head(3))

    print("\n--- Delay Sample ---")
    print(delay_df.head(3))

    print("\n--- Ticket Columns ---")
    print(ticket_df.columns.tolist())

    print("\n--- Delay Columns ---")
    print(delay_df.columns.tolist())

