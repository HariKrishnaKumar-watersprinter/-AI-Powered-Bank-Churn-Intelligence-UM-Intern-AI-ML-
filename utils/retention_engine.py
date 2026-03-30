def personalized_strategy(row, prob):

    if prob > 0.7:
        return "High Risk → Offer discount / personal manager"

    elif row["IsActiveMember"] == 0:
        return "Engagement Campaign Needed"

    elif row["NumOfProducts"] <= 1:
        return "Cross-sell products"

    elif row["Balance"] < 50000:
        return "Financial advisory + incentives"

    else:
        return "Loyalty program"