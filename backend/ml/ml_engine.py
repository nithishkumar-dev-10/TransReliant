import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import yaml
import os
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
from sklearn.metrics import f1_score,mean_absolute_error,accuracy_score,mean_squared_error,roc_auc_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder

# loading the config file 

def load_config():
    with open("backend'config.yaml","r") as f:
        return yaml.safe_load(f)
    

#load processing data

def load_data(config):
    ticket_df=pd.read_csv(config["data"]["processed"]["ticket"])
    delay_df=pd.read_csv(config["data"]["processed"]["delay"])
    
    #just print the shape to confirm no error in loading the data 
    print(f"Ticket   : {ticket_df.shape}")
    print(f"Delay    : {delay_df.shape}")

    return ticket_df,delay_df

# split the label encoding and one hot encoding columns 

def get_ticket_column_types(df, target):
    # ordered columns — label encode
    label_cols = [
        "Holiday or Peak Season",   # Yes/No has no real order but binary fine
        "journey_month",            # already numeric
        "journey_dayofweek",        # already numeric
        "days_before_journey"       # already numeric
    ]

    # no-order categorical — one hot encode
    onehot_cols = [
        "Class of Travel",
        "Quota",
        "Source Station",
        "Destination Station",
        "Train Type",
        "Special Considerations",
        "Seat Availability"
    ]

    # already numeric — pass through
    numeric_cols = [
        col for col in df.columns
        if col not in label_cols
        and col not in onehot_cols
        and col != target
    ]

    return label_cols, onehot_cols, numeric_cols


def get_delay_column_types(df, target):
    # ordered
    label_cols = [
        "Season",
        "journey_month",
        "journey_dayofweek"
    ]

    # no-order categorical
    onehot_cols = [
        "Source",
        "Destination",
        "Run_frequency"
    ]

    # already numeric
    numeric_cols = [
        col for col in df.columns
        if col not in label_cols
        and col not in onehot_cols
        and col != target
    ]

    return label_cols, onehot_cols, numeric_cols

def build_preprocessor(label_cols,onehot_cols,numeric_cols):

    label_pipeline=Pipeline(steps=[('le',OrdinalEncoder())])

    onehot_pipeline=Pipeline(steps=[("ohe",OneHotEncoder(handle_unknown='ignore'))])

    preprocessor=ColumnTransformer(transformers=[("label",label_pipeline,label_cols),("ohe",onehot_pipeline,onehot_cols),("numeric", "passthrough", numeric_cols)])

    return preprocessor
    # only the blue print is made , no real preprocessing is done here , the preprocessor will be fitted in the training function and then used for both train and test data to avoid data leakage

    