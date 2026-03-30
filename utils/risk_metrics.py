def dependency_risk(row):
    score = 0

    if row['NumOfProducts'] <= 1:
        score += 1
    if row['IsActiveMember'] == 0:
        score += 1
    if row['Balance'] > 100000.00:
        score += 1

    if score == 0:
        return "Balanced"
    elif score == 1:
        return "Medium Risk"
    else:
        return "High Risk"