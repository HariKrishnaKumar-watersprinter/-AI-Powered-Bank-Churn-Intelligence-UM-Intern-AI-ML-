def retention_action(prob):
    if prob >= 0.7:
        return "Offer premium retention package + personal manager"
    elif prob >= 0.4 and prob < 0.7:
        return "Provide targeted offers & engagement campaigns"
    else:
        return "Maintain engagement"