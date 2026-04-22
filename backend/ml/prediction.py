import joblib       # to load .pkl files
import pandas as pd # to convert dict to DataFrame
import yaml         # to read config paths

def load_config():
    with open("backend/config.yaml", "r") as f:
        return yaml.safe_load(f)
    
def load_model(config):

    #loading the model form the config file 
    classifier=joblib.load(config["model"]["classifier"]["path"])
    regressor=joblib.load(config["model"]["regressor"]["path"])

    return classifier,regressor

