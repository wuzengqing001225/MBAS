def demand_function(id, a, d, beta, price, db):
    rival_prices = db.view_other_decision_1round(id)
    d_rival_prices = 0
    for p in rival_prices:
        d_rival_prices += d * p

    if beta != d:
        if db.n_players == 2:
            b = beta * beta - d * d
            alpha = a * beta - a * d
            return (alpha - beta * price + d_rival_prices) / b
        elif db.n_players == 3:
            b = (beta - d) * (beta + 2 * d)
            alpha = a * beta - a * d
            h = beta + d
            return (alpha - h * price + d_rival_prices) / b
    else:
        if price > rival_prices[0]: return 0
        elif price < rival_prices[0]: return (a - price) / d
        else: return (a - price) / (2 * d)

def demand_function_lmax(id, a, d, beta, price, db):
    rival_prices = db.view_other_decision_lmax(id)
    d_rival_prices = 0
    for p in rival_prices:
        d_rival_prices += d * p

    if beta != d:
        if db.n_players == 2:
            b = beta * beta - d * d
            alpha = a * beta - a * d
            return (alpha - beta * price + d_rival_prices) / b
        elif db.n_players == 3:
            b = (beta - d) * (beta + 2 * d)
            alpha = a * beta - a * d
            h = beta + d
            return (alpha - h * price + d_rival_prices) / b
    
    else:
        if price > rival_prices[0]: return 0
        elif price < rival_prices[0]: return (a - price) / d
        else: return (a - price) / (2 * d)

def demand_function_umax(id, a, d, beta, price, db):
    rival_prices = db.view_other_decision_umax(id)
    d_rival_prices = 0
    for p in rival_prices:
        d_rival_prices += d * p

    if beta != d:
        if db.n_players == 2:
            b = beta * beta - d * d
            alpha = a * beta - a * d
            return (alpha - beta * price + d_rival_prices) / b
        elif db.n_players == 3:
            b = (beta - d) * (beta + 2 * d)
            alpha = a * beta - a * d
            h = beta + d
            return (alpha - h * price + d_rival_prices) / b
    
    else:
        if price > rival_prices[0]: return 0
        elif price < rival_prices[0]: return (a - price) / d
        else: return (a - price) / (2 * d)

def theoretical_price_cartelcollusion(a, d, beta, cost, db):
    if beta != d:
        if db.n_players == 2:
            alpha = a * beta - a * d
            return alpha / (2 * (beta - d)) + cost / 2
        elif db.n_players == 3:
            alpha = a * beta - a * d
            h = beta + d
            return 0 - ((alpha - 2 * cost * d + cost * h) / (2 * (2 * d - h)))
    else:
        return (a + cost) / 2

def theoretical_price_bertrand(id, a, d, beta, cost, db):
    rival_costs = db.view_other_cost(id)
    
    if beta != d:
        if db.n_players == 2:
            alpha = a * beta - a * d
            return (d * alpha + beta * d * rival_costs[0] + 2 * beta * alpha + 2 * beta * beta * cost) / (4 * beta * beta - d * d)
        elif db.n_players == 3:
            b = (beta - d) * (beta + 2 * d)
            alpha = a * beta - a * d
            h = beta + d
            dh_rival_costs = 0
            for c in rival_costs:
                dh_rival_costs += c * d * h
            return 0 - ((alpha * d + 2 * alpha * h - cost * d * h + dh_rival_costs + 2 * cost * h * h) / (2 * (d - h) * (d + 2 * h)))
    else:
        return cost

def theoretical_profit(firms, db):
    for firm in firms:
        if firm.ideal_max_lprice == -1:
            firm.ideal_max_lprice = theoretical_price_bertrand(firm.id, firm.a, firm.d, firm.beta, firm.cost, db)
        if firm.ideal_max_uprice == -1:
            firm.ideal_max_uprice = theoretical_price_cartelcollusion(firm.a, firm.d, firm.beta, firm.cost, db)
        
    for firm in firms:
        if firm.ideal_max_lprofit == -1:
            firm.ideal_max_lprofit = (firm.ideal_max_lprice - firm.cost) * demand_function_lmax(firm.id, firm.a, firm.d, firm.beta, firm.ideal_max_lprice, db)
        if firm.ideal_max_uprofit == -1:
            firm.ideal_max_uprofit = (firm.ideal_max_uprice - firm.cost) * demand_function_umax(firm.id, firm.a, firm.d, firm.beta, firm.ideal_max_uprice, db)
