from SABM.Class.worker import worker
import random

def transfer_offer(w:worker, curr_company_type, target_company_type):
    # Need Sensitivity Analysis
    accept_probability = {
        "normal": 30,
        "difficult": 10,
        "extremely_difficult": 2,
    }

    offer = random.randint(0, 100)

    if target_company_type in ["Netural", "Nymia"]:
        if offer < accept_probability["normal"]: return True
    else:
        score = 0
        if w.gender == "Nymia": score += 1
        if curr_company_type == "Nymia": score += 1

        if score == 0:
            if offer < accept_probability["normal"]: return True
        elif score == 1:
            if offer < accept_probability["difficult"]: return True
        elif score == 2:
            if offer < accept_probability["extremely_difficult"]: return True
    return False


def salary_update():
    pass