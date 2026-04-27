
from pydantic import BaseModel
from typing import Optional



class UserInput(BaseModel):
    train_number:          int
    source_station:        str
    destination_station:   str
    date_of_journey:       str
    class_of_travel:       str
    number_of_passengers:  int
    waitlist_position:     Optional[float] = 0.0



class PredictionRequest(BaseModel):
    user: UserInput