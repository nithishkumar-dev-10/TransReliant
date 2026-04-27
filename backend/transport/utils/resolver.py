
from datetime import datetime, date
from backend.transport.schemas.request import UserInput
from backend.transport.utils.train_lookup import lookup_train



def get_season(month: int) -> str:
    if month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    elif month in [10, 11]:
        return "Autumn"
    else:
        return "Winter"


def is_peak_season(month: int, dayofweek: int) -> str:
    peak_months  = [1, 4, 5, 10, 11, 12]
    peak_days    = [4, 6]  # Friday, Sunday
    if month in peak_months or dayofweek in peak_days:
        return "Yes"
    return "No"



def resolve(user: UserInput) -> tuple:


    looked_up = lookup_train(user.train_number)


    journey_date      = datetime.strptime(user.date_of_journey, "%Y-%m-%d").date()
    today             = date.today()
    journey_month     = journey_date.month
    journey_dayofweek = journey_date.weekday()
    days_before       = (journey_date - today).days


    season     = get_season(journey_month)
    peak       = is_peak_season(journey_month, journey_dayofweek)


    ticket_dict = {
        "Train Number":           user.train_number,
        "Class of Travel":        user.class_of_travel,
        "Quota":                  looked_up["Quota"],
        "Source Station":         user.source_station,
        "Destination Station":    user.destination_station,
        "Number of Passengers":   user.number_of_passengers,
        "Travel Distance":        looked_up["Travel_Distance"],
        "Number of Stations":     looked_up["Number_of_Stations"],
        "Travel Time":            looked_up["Travel_Time"],
        "Train Type":             looked_up["Train_Type"],
        "Seat Availability":      looked_up["Seat_Availability"],
        "Special Considerations": looked_up["Special_Considerations"],
        "Holiday or Peak Season": peak,
        "Waitlist Position":      user.waitlist_position,
        "journey_month":          journey_month,
        "journey_dayofweek":      journey_dayofweek,
        "days_before_journey":    days_before,
    }


    delay_dict = {
        "Train_no":          user.train_number,
        "Source":            user.source_station,
        "Destination":       user.destination_station,
        "Distance(Km)":      looked_up["Distance_Km"],
        "Season":            season,
        "Run_frequency":     looked_up["Run_frequency"],
        "journey_month":     journey_month,
        "journey_dayofweek": journey_dayofweek,
    }


    return ticket_dict, delay_dict