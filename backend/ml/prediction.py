import joblib       # to load .pkl files
import pandas as pd # to convert dict to DataFrame
import yaml         # to read config paths

def load_config():
    with open("backend/config.yaml", "r") as f:
        return yaml.safe_load(f)
    
def load_model(config):

    #loading the model form the config file 
    classifier=joblib.load(config["models"]["classifier"]["path"])
    regressor=joblib.load(config["models"]["regressor"]["path"])

    return classifier,regressor

def predict_confirmation(classifier, input_data: dict) -> dict:
    df         = pd.DataFrame([input_data])
    prob       = classifier.predict_proba(df)[:, 1][0]
    percentage = round(float(prob) * 100, 2)

    return {
        "confirmation_probability": percentage,
        "confirmation_label": (
            "High"   if percentage >= 75 else
            "Medium" if percentage >= 40 else
            "Low"
        )
    }

def predict_delay(regressor, input_data: dict) -> dict:
    df    = pd.DataFrame([input_data])
    delay = max(float(regressor.predict(df)[0]), 0)

    hours   = int(delay // 60)
    minutes = int(delay % 60)

    return {
        "delay_minutes":  round(delay, 2),
        "delay_readable": f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m",
        "delay_label": (
            "On Time"  if delay <= 15  else
            "Slight"   if delay <= 45  else
            "Moderate" if delay <= 120 else
            "Severe"
        )
    }

if __name__ == "__main__":
    config = load_config()
    classifier, regressor = load_model(config)

    ticket_input = {
        "Train Number":           12238,
        "Class of Travel":        "3AC",
        "Quota":                  "General",
        "Source Station":         "NDLS",
        "Destination Station":    "CSMT",
        "Number of Passengers":   2,
        "Travel Distance":        1400,
        "Number of Stations":     15,
        "Travel Time":            30,
        "Train Type":             "Rajdhani",
        "Seat Availability":      120,
        "Special Considerations": "None",
        "Holiday or Peak Season": "Yes",
        "Waitlist Position":      45,
        "journey_month":          9,
        "journey_dayofweek":      4,
        "days_before_journey":    30
    }

    delay_input = {
        "Train_no":          12238,
        "Source":            "Varanasi",
        "Destination":       "Jammu",
        "Distance(Km)":      1260,
        "Season":            "Winter",
        "Run_frequency":     "Daily",
        "journey_month":     1,
        "journey_dayofweek": 4
    }

    conf_result  = predict_confirmation(classifier, ticket_input)
    delay_result = predict_delay(regressor, delay_input)

    print("\n--- Prediction Results ---")
    print(f"Confirmation : {conf_result['confirmation_probability']}% ({conf_result['confirmation_label']})")
    print(f"Delay        : {delay_result['delay_readable']} — {delay_result['delay_label']}")
    print(f"Delay (raw)  : {delay_result['delay_minutes']} minutes")