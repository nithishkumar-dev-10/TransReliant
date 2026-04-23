from pydantic import BaseModel
from typing import Optional 

class TicketPredictionResponse(BaseModel):
    confirmation_probability: float
    confirmation_label: str

class DelayPredictionResponse(BaseModel):
    delay_minutes:float
    delay_readable:str
    delay_label:str

class RelialbiltyRespose(BaseModel):
    score: float
    label: str
    confirmation_used: float
    delay_minutes: float
    delay_reliability: float
    historical_score: float

class FullResponse(BaseModel):
    ticket: TicketPredictionResponse
    delay: DelayPredictionResponse
    reliability: RelialbiltyRespose
    