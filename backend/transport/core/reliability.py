import yaml

import os

def load_config():
    # get path relative to project root regardless of where you run from
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(base_dir, "config.yaml")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def delay_to_reliability(delay_minutes: float) -> float:
    # Indian Railways context:
    

    if delay_minutes <= 30:
        # very common — almost no penalty
        score = 100 - (delay_minutes * 0.5)

    elif delay_minutes <= 60:
        # slight delay — small penalty
        score = 85 - ((delay_minutes - 30) * 1.0)

    elif delay_minutes <= 120:
        # moderate delay — medium penalty
        score = 55 - ((delay_minutes - 60) * 1.5)

    else:
        # severe delay — heavy penalty, min 0
        score = 10 - ((delay_minutes - 120) * 0.5)

    return round(max(0.0, score), 2)

def get_historical_score(source: str, destination: str) -> float:
    known_routes = {
        ("NDLS", "CSMT"): 80.0,
        ("CSMT", "NDLS"): 78.0,
        ("NDLS", "HWH"):  72.0,
        ("MAS",  "NDLS"): 65.0,
        ("NDLS", "BCT"):  75.0,
        ("BCT",  "NDLS"): 74.0,
    }
    key = (source.upper(), destination.upper())
    return known_routes.get(key, 68.0)
    # 68 default — Indian Railways average reliability



def calculate_reliability(confirmation_probability: float, delay_minutes: float, source: str, destination: str) -> float:
    config=load_config()

    historical_score=get_historical_score(source,destination)

    delay_score=delay_to_reliability(delay_minutes)

    weights=config["reliability"]["weights"]

    conf_score=confirmation_probability

    final_score = round(
        (conf_score       * weights["confirmation"]) +
        (delay_score      * weights["delay"])        +
        (historical_score * weights["historical"]),
        2
    )

    if final_score>=80:
        label="High Reliability"
    
    elif final_score>=50:
        label="Moderate Reliability"

    elif final_score>=30:
        label="Low Reliability"

    else:
        label="Very Low Reliability"

    return {
        "score":             final_score,
        "label":             label,
        "confirmation_used": confirmation_probability,
        "delay_minutes":     delay_minutes,
        "delay_reliability": delay_score,
        "historical_score":  historical_score
    }



if __name__ == "__main__":
    result = calculate_reliability(
        confirmation_probability=77.34,
        delay_minutes=25.3,
        source="NDLS",
        destination="CSMT"
    )

    print("\n--- Reliability Score ---")
    print(f"Score             : {result['score']} / 100")
    print(f"Label             : {result['label']}")
    print(f"Confirmation      : {result['confirmation_used']}%")
    print(f"Delay Reliability : {result['delay_reliability']} / 100")
    print(f"Historical Score  : {result['historical_score']} / 100")
