
from backend.transport.schemas.request import UserInput
from backend.transport.utils.resolver import resolve
from backend.ml.prediction import predict_confirmation, predict_delay, load_model, load_config
from backend.transport.core.reliability import calculate_reliability



config                = load_config()
classifier, regressor = load_model(config)


async def run_prediction_service(user: UserInput) -> dict:


    ticket_dict, delay_dict = resolve(user)

    
    conf_result  = predict_confirmation(classifier, ticket_dict)
    delay_result = predict_delay(regressor, delay_dict)

    
    conf_prob   = conf_result["confirmation_probability"]
    delay_min   = delay_result["delay_minutes"]
    source      = user.source_station
    destination = user.destination_station

    
    reliability_result = calculate_reliability(
        confirmation_probability = conf_prob,
        delay_minutes            = delay_min,
        source                   = source,
        destination              = destination
    )

    
    return {
        "ticket":      conf_result,
        "delay":       delay_result,
        "reliability": reliability_result
    }