from SABM.Class.firm import firm
from typing import List
from SABM.Utils.Implement_Tools import display
from SABM.Prompt.prompt import task_prompt

class database():
    def __init__(self, firms:List[firm]):
        self.firms = firms
        self.n_players = len(firms)
        
        self.round_communication_context = ""
        self.communication_context = []

        self.decision_history = {i: [] for i in range(1, self.n_players + 1)}
    
    def numerical_history(data, type = 'simple_round', sep = ',', label = ''):
        history = ""
        for index in range(len(data)):
            if type == 'round':
                history += f'Round {index + 1}: {data[index]}\n'
            elif type == 'simple_round':
                history += f'{data[index]}'
                if index != len(data) - 1: history += sep + ' '
        return history
    
    def view_other_cost(self, self_id):
        rival_costs = []
        for firm in self.firms:
            if firm.id == self_id:
                pass
            else:
                rival_costs.append(firm.cost)
        return rival_costs
    
    def view_other_decision_lmax(self, self_id):
        rival_prices = []
        for firm in self.firms:
            if firm.id == self_id:
                pass
            else:
                rival_prices.append(firm.ideal_max_lprice)
        return rival_prices

    def view_other_decision_umax(self, self_id):
        rival_prices = []
        for firm in self.firms:
            if firm.id == self_id:
                pass
            else:
                rival_prices.append(firm.ideal_max_uprice)
        return rival_prices

    def view_other_decision_1round(self, self_id):
        rival_prices = []
        for firm in self.firms:
            if firm.id == self_id:
                pass
            else:
                rival_prices.append(firm.price)
        return rival_prices

    def view_other_decision_history_1round(self, self_id, i):
        price_history = ""
        for firm in self.firms:
            if firm.id == self_id:
                pass
            else:
                price_history += f"Firm {firm.firm_name} Price {firm.history['price_history'][i - 1]} "
        return price_history
    
    def view_decision_history(self, self_id, loop_round, history_range):
        decision_history = task_prompt['history']['history_decision'].format(previous_rounds = len(range(max(0, loop_round - history_range - 1), loop_round - 1)))

        for firm in self.firms:
            if firm.id == self_id:
                for i in range(max(1, loop_round - history_range), loop_round):
                    decision_history += f"Round #{i}: {firm.history['price_history'][i - 1]}, {display.round_function(firm.history['demand_history'][i - 1])}, {display.round_function(firm.history['profit_history'][i - 1])}, {firm.history['asset_history'][i - 1]}, {self.view_other_decision_history_1round(self_id, i)}\n"
                return decision_history
    
    def view_other_stat_history(self, self_id, lround, rround):
        price_history = ""
        for firm in self.firms:
            if firm.id == self_id:
                pass
            else:
                price_history += f"Firm {firm.firm_name} Avg Price {display.round_function(float(sum(firm.history['price_history'][lround : rround])) / len(firm.history['price_history'][lround : rround]))} "
        return price_history
    
    def view_statistics_bin_history(self, self_id, loop_round, history_range):
        bin_history = task_prompt['history']['history_bin']

        for firm in self.firms:
            if firm.id == self_id:
                for i in range(max(0, int(loop_round / history_range) - history_range), int(loop_round / history_range)):
                    lround = i * history_range
                    rround = (i + 1) * history_range
                    data_len = len(firm.history['profit_history'][lround : rround])
                    bin_history += task_prompt['history']["history_bin_format"].format(
                        lround = lround + 1,
                        rround = rround,
                        avgPrice = display.round_function(
                            float(sum(firm.history['price_history'][lround : rround])) / data_len),
                        avgDemand = display.round_function(
                            float(sum(firm.history['demand_history'][lround : rround])) / data_len),
                        avgProfit = display.round_function(
                            float(sum(firm.history['profit_history'][lround : rround])) / data_len),
                        avgAsset = display.round_function(
                            float(sum(firm.history['asset_history'][lround : rround])) / data_len),
                        other_firm_avgPrices = self.view_other_stat_history(self_id, lround, rround)
                    ) + '\n'
        
        return bin_history + '\n'
        