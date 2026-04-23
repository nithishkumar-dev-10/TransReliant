# Part 1 — Imports
# Bringing in both input schemas so we can type the function parameters properly
from backend.transport.schemas.request import TicketInput, DelayInput


# Part 2 — encode_ticket_input
# Converts TicketInput Pydantic object into exact dict the classifier was trained on
def encode_ticket_input(ticket: TicketInput) -> dict:
    return {
        "Train Number":           ticket.Train_Number,
        "Class of Travel":        ticket.Class_of_Travel,
        "Quota":                  ticket.Quota,
        "Source Station":         ticket.Source_Station,
        "Destination Station":    ticket.Destination_Station,
        "Number of Passengers":   ticket.Number_of_Passengers,
        "Travel Distance":        ticket.Travel_Distance,
        "Number of Stations":     ticket.Number_of_Stations,
        "Travel Time":            ticket.Travel_Time,
        "Train Type":             ticket.Train_Type,
        "Seat Availability":      ticket.Seat_Availability,
        "Special Considerations": ticket.Special_Considerations,
        "Holiday or Peak Season": ticket.Holiday_or_Peak_Season,
        "Waitlist Position":      ticket.Waitlist_Position,
        "journey_month":          ticket.journey_month,
        "journey_dayofweek":      ticket.journey_dayofweek,
        "days_before_journey":    ticket.days_before_journey,
    }


# Part 3 — encode_delay_input
# Converts DelayInput Pydantic object into exact dict the regressor was trained on
def encode_delay_input(delay: DelayInput) -> dict:
    return {
        "Train_no":          delay.Train_no,
        "Source":            delay.Source,
        "Destination":       delay.Destination,
        "Distance(Km)":      delay.Distance_Km,
        "Season":            delay.Season,
        "Run_frequency":     delay.Run_frequency,
        "journey_month":     delay.journey_month,
        "journey_dayofweek": delay.journey_dayofweek,
    }