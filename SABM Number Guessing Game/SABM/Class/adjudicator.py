from SABM.Class.agent import Agent
from SABM.Utils.Text_Processing import format_prompt
from SABM.Utils.Text_Processing import format_response
from SABM.Utils.Implement_Tools import display

class adjudicator(Agent):
    def __init__(self, id, type = 'adjudicator', target_number = 0, temperature=1.0, model='gpt-3.5-turbo', max_tokens=256, api_key = ''):
        Agent.__init__(self, type=type, id=id, temperature=temperature, model=model, max_tokens=max_tokens, api_key = api_key)
        self.target_number = target_number

    def adjudicator_first_round(self, task_parameters):
        order_set = task_parameters['order_set']
        range_begin = task_parameters['range_begin'] 
        range_end = task_parameters['range_end']
        prompt = {
            "type": "adjudicator",
            "description": "",
            "command": "task, role adjudicator, action adjudicator -newline, output number",
            "value":{
                "task": {},
                "role": {},
                "history": {},
                "action": {'range_begin': range_begin, 'range_end': range_end},
                "output": {},
            }
        }

        prompt = format_prompt.link_prompt(prompt, order_set)
        response = self.communicate(prompt)

        if task_parameters["prompt_display"]: display.display(self, prompt, 'i')
        if task_parameters["response_display"]: display.display(self, response, 'o')

        self.target_number = format_response.match_number_int(response)

        return self.target_number
    
    def adjudicator_continue(self, task_parameters, info):
        order_set = task_parameters['order_set']
        range_begin = task_parameters['range_begin'] 
        range_end = task_parameters['range_end']
        guess = info['guess']
        prompt = {
            "type": "adjudicator",
            "description": "",
            "command": "role adjudicator continue, history adjudicator target_number, history adjudicator guesser_guess, action adjudicator judge, output judge",
            "value":{
                "task": {},
                "role": {},
                "history": {'target_number': self.target_number, 'guess': guess},
                "action": {'range_begin': range_begin, 'range_end': range_end},
                "output": {},
            }
        }
        
        prompt = format_prompt.link_prompt(prompt, order_set)
        response = self.communicate(prompt)

        if task_parameters["prompt_display"]: display.display(self, prompt, 'i')
        if task_parameters["response_display"]: display.display(self, response, 'o')

        return response
