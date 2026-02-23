def calculate_risk(volatility):
    if volatility < 0.15:
        return "Low"
    elif volatility < 0.25:
        return "Moderate"
    else:
        return "High"
