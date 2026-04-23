from pydantic import BaseModel
from typing import Optional

class TicketInput(BaseModel):
    Train_Number: int
    Class_of_Travel: str
    Quota: str
    Source_Station: str
    Destination_Station: str
    Number_of_Passengers: int
    Travel_Distance: float
    Number_of_Stations: int
    Travel_Time: float
    Train_Type: str
    Seat_Availability: str
    Special_Considerations: str
    Holiday_or_Peak_Season: str
    Waitlist_Position: float
    journey_month: int
    journey_dayofweek: int
    days_before_journey: int

class DelayInput(BaseModel):
    Train_no: int
    Source: str
    Destination: str
    Distance_Km: float
    Season: str
    Run_frequency: str
    journey_month: int
    journey_dayofweek: int


class PredictionRequest(BaseModel):
    ticket: TicketInput
    delay:  DelayInput
