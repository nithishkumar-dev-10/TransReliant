from backend.transport.schemas.request import TicketInput, DelayInput
from backend.transport.utils.feature_encoder import encode_ticket_input, encode_delay_input
from backend.ml.prediction import load_config, load_model, predict_confirmation, predict_delay
from backend.transport.core.reliability import calculate_reliability

config=load_config()
classifier, regressor = load_model(config)

async def run_prediction_service(ticket_input: TicketInput, delay_input: DelayInput):
    # Step 1: Encode inputs
    tickect_dict=encode_ticket_input(ticket_input)
    delay_dict=encode_delay_input(delay_input)

    #step2 : using the models
    conf_result=predict_confirmation(classifier,tickect_dict)
    delay_result=predict_delay(regressor,delay_dict)

    conf_prob=conf_result["confirmation_probability"]
    delay_min=delay_result["delay_minutes"]
    source=delay_input.Source
    destination=delay_input.Destination

    #step_3 : calculate reliablity
    reliability_result=calculate_reliability(
        confirmation_probability=conf_prob,
        delay_minutes=delay_min,
        source=source,
        destination=destination
    )

    return {
        "ticket":conf_result,
        "delay":delay_result,
        "reliability":reliability_result
    }




