


def cost_function(y_true, y_pred):
    cost = 0

    for yt, yp in zip(y_true, y_pred):

        if yt == 1 and yp == 0:
            cost += 500   # missed churn

        elif yt == 0 and yp == 1:
            cost += 50    # unnecessary retention

    return cost