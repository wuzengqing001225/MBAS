from SABM.Class.agent import Agent
from SABM.Utils.Text_Processing import format_prompt
from SABM.Utils.Text_Processing import format_response
from SABM.Utils.Implement_Tools import display
from SABM.Utils.Text_Processing import calculation
import textwrap

class worker(Agent):
    def __init__(self, id,
                 gender, background, job,
                 fixed_expenditure = 40000, asset = 10000,
                 temperature=1.0, model='gpt-3.5-turbo', max_tokens=128, api_key = ''):
        Agent.__init__(self, type=f"{gender} worker", id=id, temperature=temperature, model=model, max_tokens=max_tokens, api_key = api_key)

        # Static Properties
        self.gender:str = gender
        self.background:dict = background

        # Dynamic Properties
        self.job:str = job
        self.income:int = 0
        self.fixed_expenditure:int = fixed_expenditure
        self.asset:int = asset

        # Persona
        self.persona:str = ""

        # History data
        self.response_history = []
        self.transfer_history = []
        self.income_history = []

        # Prompt
        self.context_prompt:str = ""
        self.command:dict = {}
    
    def info_display(self):
        info = f"""
            {self.type}
            [Job Type] {self.job}
            [Persona] {self.persona}
            [Income] {self.income}
            [Asset] {self.asset}
            [Transfer History] {format_prompt.format_transfer_history(self.transfer_history)}"""
        print(textwrap.dedent(info))
    
    def init_command(self, task_parameters):
        command_set = {
            "background": f"task 0 -newline, role default",
            "evaluation_current": f"history self company -newline, action evaluation self, output limit",
            "evaluation_other": f"history other companies -newline, action evaluation other, output evaluation other, output limit",
            "decision_transfer": f"history evaluation, action decision transfer -newline, output bool",
            "decision_transfer_target": f"history evaluation target -newline, action decision target -newline, output number target, output ban",
        }

        self.command['background'] = command_set['background']
        self.command['evaluation_current'] = command_set['evaluation_current']
        self.command['evaluation_other'] = command_set['evaluation_other']
        self.command['decision_transfer'] = command_set['decision_transfer']
        self.command['decision_transfer_target'] = command_set['decision_transfer_target']
    
    def background_prompt(self, task_parameters):
        order_set = task_parameters['order_set']
        background_prompt = {
            "type": "worker",
            "description": "",
            "command": self.command['background'],
            "value": {
                "task": {},
                "role": {"worker_type": self.type},
                "history": {},
                "action": {},
                "output": {},
                "rule": {},
            }
        }
        background_prompt = format_prompt.link_prompt(background_prompt, order_set)
        return background_prompt + '\n\n'
    
    def evaluation_current(self, task_parameters, info):
        order_set = task_parameters['order_set']
        evaluation_current_prompt = {
            "type": "worker",
            "description": "",
            "command": self.command['evaluation_current'],
            "value": {
                "task": {},
                "role": {},
                "history": {"salary": self.income, "percentage": calculation.calu_salary_bin(info['all_salaries'], self.income), "increase_amount": calculation.calu_income_difference(self.income_history), "comparison": calculation.calu_increase_bin(info['all_increases'], calculation.calu_income_difference(self.income_history)), "gender_ratio": info['self_gender_ratio']},
                "action": {},
                "output": {"limit_token": 100},
                "rule": {},
            }
        }
        prompt = self.context_prompt + format_prompt.link_prompt(evaluation_current_prompt, order_set)
        response = self.communicate(prompt)
    
        if task_parameters["prompt_display"]: display.display(self, prompt, 'i')
        if task_parameters["response_display"]: display.display(self, response, 'o', 'evaluation current')

        self.response_history[-1]['evaluation_current'] = response

        return response
    
    def evaluation_other(self, task_parameters, info):
        order_set = task_parameters['order_set']
        evaluation_other_prompt = {
            "type": "worker",
            "description": "",
            "command": self.command['evaluation_other'],
            "value": {
                "task": {},
                "role": {},
                "history": {"salary": self.income, "percentage": calculation.calu_salary_bin(info['all_salaries'], self.income), "companies_data": info['other_company_data']},
                "action": {},
                "output": {"limit_token": 100},
                "rule": {},
            }
        }
        prompt = self.context_prompt + format_prompt.link_prompt(evaluation_other_prompt, order_set)
        response = self.communicate(prompt)
    
        if task_parameters["prompt_display"]: display.display(self, prompt, 'i')
        if task_parameters["response_display"]: display.display(self, response, 'o', 'evaluation other')

        self.response_history[-1]['evaluation_other'] = response

        return response
    
    def decision_transfer(self, task_parameters, info):
        order_set = task_parameters['order_set']
        decision_transfer_prompt = {
            "type": "worker",
            "description": "",
            "command": self.command['decision_transfer'],
            "value": {
                "task": {},
                "role": {},
                "history": {'self_eval': self.response_history[-1]['evaluation_current'], 'other_eval': self.response_history[-1]['evaluation_other']},
                "action": {},
                "output": {},
                "rule": {},
            }
        }
        prompt = self.context_prompt + format_prompt.link_prompt(decision_transfer_prompt, order_set)
        response = self.communicate(prompt)
    
        if task_parameters["prompt_display"]: display.display(self, prompt, 'i')
        if task_parameters["response_display"]: display.display(self, response, 'o', 'transfer decision')
        
        response = format_response.match_bool_yn(response)
        self.response_history[-1]['decision_transfer'] = response

        return response

    def decision_transfer_target(self, task_parameters, info):
        order_set = task_parameters['order_set']
        decision_transfer_target_prompt = {
            "type": "worker",
            "description": "",
            "command": self.command['decision_transfer_target'],
            "value": {
                "task": {},
                "role": {},
                "history": {'other_eval': self.response_history[-1]['evaluation_other']},
                "action": {'target_list': info['other_company_names']},
                "output": {},
                "rule": {},
            }
        }
        prompt = self.context_prompt + format_prompt.link_prompt(decision_transfer_target_prompt, order_set)
        response = self.communicate(prompt)
    
        if task_parameters["prompt_display"]: display.display(self, prompt, 'i')
        if task_parameters["response_display"]: display.display(self, response, 'o', 'transfer decision')
        
        response = format_response.match_number_int(response, 1, len(info['other_company_names']), 1)
        self.response_history[-1]['decision_transfer_target'] = response

        return response
    
    def update_income(self, income):
        self.income = income
        self.income_history.append(self.income)

    def update_asset(self):
        self.asset += self.income - self.fixed_expenditure
