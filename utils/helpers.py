def risk_segment(prob):
    if prob < 0.3:
        return "Low Risk"
    elif prob < 0.5:
        return "Medium Risk"
    else:
        return "High Risk"