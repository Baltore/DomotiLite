from datetime import datetime

def is_night():
    current_hour = datetime.now().hour
    return current_hour < 6 or current_hour >= 20  # Nuit : 20h - 6h

def evaluate_rules(sensor_data):
    actions = []

    temp = sensor_data.get("temperature")
    light = sensor_data.get("luminosity")

    # Température
    if temp is not None:
        if temp > 26:
            actions.append(("climatisation", "ON"))
        elif temp < 19:
            actions.append(("chauffage", "ON"))

    # Luminosité avec cycle jour/nuit
    if light is not None:
        if light > 80:
            actions.append(("volets", "OFF"))  # trop de lumière → fermer
        elif light < 20:
            if is_night():
                actions.append(("lumière", "ON"))
            else:
                actions.append(("volets", "ON"))

    return actions
