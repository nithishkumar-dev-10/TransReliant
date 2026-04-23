# Part 1 — Imports
# Bringing in the core reliability logic to wrap in a service layer
from core.reliability import calculate_reliability


# Part 2 — get_reliability
# Thin wrapper that gives reliability its own clean service layer
def get_reliability(confirmation_probability: float,delay_minutes: float,source: str,destination: str) -> dict:

    # Call core reliability logic and return result directly
    return calculate_reliability(
        confirmation_probability = confirmation_probability,
        delay_minutes            = delay_minutes,
        source                   = source,
        destination              = destination
    )

