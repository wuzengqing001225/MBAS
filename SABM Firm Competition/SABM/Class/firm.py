from SABM.Class.agent import Agent
from SABM.Utils.Text_Processing import format_prompt
from SABM.Utils.Text_Processing import format_response
from SABM.Utils.Implement_Tools import display
import SABM.Class.theoretical_rules as rules

class firm(Agent):
    def __init__(self, id, firm_name, cost, a, d, beta,
                 total_asset, fixed_expenditure, persona:str,
                 type = 'firm',
                 temperature=0.7, model='gpt-3.5-turbo', max_tokens=128, api_key = ''):
        Agent.__init__(self, type=type, id=id, temperature=temperature, model=model, max_tokens=max_tokens, api_key = api_key)

        # Properties
        self.cost = cost
        self.a = a
        self.d = d
        self.beta = beta
        self.total_asset = total_asset
        self.fixed_expenditure = fixed_expenditure

        # Persona
        self.persona = persona
        self.firm_name = firm_name

        # Round data
        self.price:     float = 0
        self.profit:    float = 0
        self.demand:    float = 0

        # History data
        self.strategy = []
        self.history = {
            "price_history": [],
            "demand_history": [],
            "profit_history": [],
            "asset_history": []
        }
        self.max_updated_history = []

        self.context_prompt = ""
        self.command = {}

        self.max_profit = 0
        self.max_price = 0
        
        self.ideal_max_lprice = -1
        self.ideal_max_uprice = -1
        self.ideal_max_lprofit = -1
        self.ideal_max_uprofit = -1
        
    def calc_demand(self, db):
        self.demand = rules.demand_function(self.id, self.a, self.d, self.beta, self.price, db)
        if self.demand < 0:
            self.demand = 0
            display.display_error("Demand < 0", "Firm {self.id} calc_demand", "Theorical")
        self.history['demand_history'].append(self.demand)
        return self.demand

    def calc_profit(self, info):
        self.profit = int((self.price - self.cost) * self.demand)
        if self.profit > self.max_profit:
            self.max_profit = self.profit
            self.max_price = self.price
            self.max_updated_history.append(info['loop_round'])
        self.history['profit_history'].append(self.profit)
        return self.profit

    def calc_asset(self):
        self.total_asset = self.total_asset - self.fixed_expenditure + self.profit
        self.history['asset_history'].append(self.total_asset)
        return self.total_asset
    
    def init_command(self, task_parameters):
        command_set = {
            #"background_2": f"""task title -newline, task twoplayer, role twoplayer -newline2, history asset -newline, rule profit, role persona {self.persona}""",
            #"background_3": f"""task title -newline, task threeplayer role threeplayer -newline2, history asset -newline, rule profit, role persona {self.persona}""",
            "background_2": f"""task twoplayer, role twoplayer -newline2, history asset -newline, rule profit, role persona {self.persona}""",
            "background_3": f"""task threeplayer role threeplayer -newline2, history asset -newline, rule profit, role persona {self.persona}""",
            "communication": f"role -newline, task {task_parameters['task']}, output notice",
            "strategy_communication": "action context -newline, role -newline, action context conversation, action strategy",
            "strategy_default": "action context -newline, role -newline, action strategy",
            "decision_communication": "action context -newline, role -newline, action context conversation -newline, action context strategy -newline, action decision, output price, output price 2",
            "decision_default": "action context -newline, role -newline, action context strategy -newline, action decision, output price, output price 2",
        }

        if task_parameters['n_players'] == 2: self.command['background'] = command_set['background_2']
        elif task_parameters['n_players'] == 3: self.command['background'] = command_set['background_3']
        
        self.command['communication'] = command_set['communication']

        if task_parameters['communication']: self.command['strategy'] = command_set['strategy_communication']
        else: self.command['strategy'] = command_set['strategy_default']

        if task_parameters['communication']: self.command['decision'] = command_set['decision_communication']
        else: self.command['decision'] = command_set['decision_default']

    
    def background_prompt(self, task_parameters, db):
        order_set = task_parameters['order_set']
        background_prompt = {
            "type": "firm",
            "description": "",
            "command": self.command['background'],
            "value": {
                "task": {},
                "role": {"firm_name": self.firm_name, "other_firm_names" : format_prompt.format_other_firm_name(self.firm_name, task_parameters['dictionary']['firm_name'], db.n_players)},
                "history": {"asset": self.total_asset, "expenditure": self.fixed_expenditure, "diff_asset": self.total_asset - self.fixed_expenditure},
                "action": {},
                "output": {},
                "rule": {},
            }
        }
        background_prompt = format_prompt.link_prompt(background_prompt, order_set)
        return background_prompt + '\n\n'
    
    def historical_decisions(self, task_parameters, info, db):
        history_range = task_parameters['history_range']
        loop_round = info['loop_round']
        
        decision_history = ""

        if loop_round != 1:
            # Statistical History (bins)
            if loop_round >= history_range and loop_round % history_range == 1:
                decision_history = db.view_statistics_bin_history(self.id, loop_round, history_range)

            # Decision History
            decision_history += db.view_decision_history(self.id, loop_round, history_range)

        return decision_history + '\n'
    
    def firm_communication(self, task_parameters, info):
        order_set = task_parameters['order_set']

        prompt = {
            "type": "firm",
            "description": "",
            "command": self.command['communication'],
            "value": {
                "task": {},
                "role": {"firm_name": self.firm_name, "current_round": info['loop_round']},
                "history": {},
                "action": {},
                "output": {},
                "rule": {},
            }
        }

        prompt = self.context_prompt + format_prompt.format_strategy_1round(self.strategy) + \
            format_prompt.link_prompt(prompt, order_set) + \
            format_prompt.format_conversation(info['communication_context'])
        
        response = self.communicate(prompt)
        response = f"Firm {self.firm_name}: {response}\n"

        if task_parameters["prompt_display"]: display.display(self, prompt, 'i')
        if task_parameters["response_display"]: display.display(self, response, 'o', 'communication')

        return response
    
    def generate_strategy(self, task_parameters, info):
        order_set = task_parameters['order_set']

        prompt = {
            "type": "firm",
            "description": "",
            "command": self.command['strategy'],
            "value": {
                "task": {},
                "role": {"firm_name": self.firm_name, "current_round": info['loop_round']},
                "history": {},
                "action": {"context": self.context_prompt, "conversation": info['communication_context'], "previous_strategy": format_prompt.format_strategy(self.strategy, task_parameters['history_range'])},
                "output": {},
                "rule": {},
            }
        }

        prompt = format_prompt.link_prompt(prompt, order_set)
        response = self.communicate(prompt)
        response = f"Round #{info['loop_round']}: {response}"

        if task_parameters["prompt_display"]: display.display(self, prompt, 'i')
        if task_parameters["response_display"]: display.display(self, response, 'o', 'strategy')

        self.strategy.append(response)

        return response
    
    def choice_price(self, task_parameters, info):
        order_set = task_parameters['order_set']
        
        prompt = {
            "type": "firm",
            "description": "",
            "command": self.command['decision'],
            "value": {
                "task": {},
                "role": {"firm_name": self.firm_name, "current_round": info['loop_round']},
                "history": {},
                "action": {"context": self.context_prompt, "conversation": info['communication_context'], "strategy": format_prompt.format_strategy_1round(self.strategy)},
                "output": {"firm_a": self.a},
                "rule": {},
            }
        }

        prompt = format_prompt.link_prompt(prompt, order_set)
        response = self.communicate(prompt)

        if task_parameters["prompt_display"]: display.display(self, prompt, 'i')
        if task_parameters["response_display"]: display.display(self, response, 'o')

        self.price = format_response.match_number_float(response, exception=self.cost)
        if self.price < self.cost: self.price = self.cost
        self.history['price_history'].append(self.price)
        return self.price
