from SABM.Class.agent import Agent
from SABM.Utils.Format import format_history
from SABM.Utils.Text_Processing import format_prompt
from SABM.Utils.Text_Processing import format_response
from SABM.Utils.Implement_Tools import display

class guesser(Agent):
    def __init__(self, id, type = 'guesser', target_number = 0, temperature=1.0, model='gpt-3.5-turbo', max_tokens=256, api_key = ''):
        Agent.__init__(self, type=type, id=id, temperature=temperature, model=model, max_tokens=max_tokens, api_key = api_key)
        self.previous_guess = 0
        self.guess_history = []

    def guesser_first_round(self, task_parameters):
        order_set = task_parameters['order_set']
        range_begin = task_parameters['range_begin']
        range_end = task_parameters['range_end']
        prompt = {
            "type": "guesser",
            "description": "",
            "command": "task default, role guesser, action guesser, output guess",
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
        
        self.previous_guess = format_response.match_number_int(response)
        self.guess_history.append(self.previous_guess)

        return self.previous_guess

    def guesser_continue(self, task_parameters, info):
        order_set = task_parameters['order_set']
        range_begin = task_parameters['range_begin']
        range_end = task_parameters['range_end']

        previous_guess_result = f"{self.previous_guess}, {info['judgment'].lower()}"

        prompt = {
            "type": "guesser",
            "description": "",
            "command": "role guesser continue, action guesser continue, history guesser previous_one_guess, history guesser guess_history, output guess",
            "value":{
                "task": {},
                "role": {},
                "history": {'previous_guess': previous_guess_result, 'guess_history': format_history.numerical_history(self.guess_history)},
                "action": {'range_begin': range_begin, 'range_end': range_end},
                "output": {},
            }
        }

        prompt = format_prompt.link_prompt(prompt, order_set)
        response = self.communicate(prompt)

        if task_parameters["prompt_display"]: display.display(self, prompt, 'i')
        if task_parameters["response_display"]: display.display(self, response, 'o')

        self.previous_guess = format_response.match_number_int(response)
        self.guess_history.append(self.previous_guess)

        return self.previous_guess
