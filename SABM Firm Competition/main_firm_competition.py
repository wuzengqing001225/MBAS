from workflow_firm_competition_ISR import task
from SABM.Utils.IO import data_output

api_key = "sk-"

persona_dictionary = ['none', 'active', 'aggressive']
firm_name_dictionary = ['Ed', 'Gill', 'Celia']

task_parameters = {
    # Model
    "model": 'gpt-4-0314',
    "max_tokens": 128,
    
    "dictionary": {
        "persona": persona_dictionary,
        "firm_name": firm_name_dictionary,
    },

    "output_path": "{record_path}/{record_name}",

    # Load Data
    "load_data": True,
    "load_data_name": "",

    # Command Set for Prompt
    "order_set": ['task', 'role', 'history', 'action', 'output', 'rule'],

    # Simulation Loop
    "loop_max": 2000,
    "loop_breakpoint": 100,      # Default = 50
    "history_range": 20,        # Default = 20
    "start_round": 1,          # Default = 1
    
    # Task Specific Parameters
    ## Task
    "task": "0",                # 1 to 3, 0 is the origin

    ## Number of Players
    "n_players": 2,

    ## Communication
    "communication": False,
    "communication_rounds": 3,  # Default = 3
    
    ## Price
    "set_initial_price": True,
    "initial_price":{
        1: 2,
        2: 2,
        3: 2,
    },
    
    "firm_parameter": {
        1: {
            "name": "Ed",
            "cost": 2,
            "a": 14,
            "d": 0.00333333333333,
            "beta": 0.00666666666666,
            "initial_price": 2,
            "total_asset": 10000,
            "fixed_expenditure": 3000,
            "persona": persona_dictionary[0]
        },
        2: {
            "name": "Gill",
            "cost": 2,
            "a": 14,
            "d": 0.00333333333333,
            "beta": 0.00666666666666,
            "initial_price": 2,
            "total_asset": 10000,
            "fixed_expenditure": 3000,
            "persona": persona_dictionary[0]
        },
        3: {
            "name": "Celia",
            "cost": 2,
            "a": 14,
            "d": 0.00333333333333,
            "beta": 0.00666666666666,
            "initial_price": 2,
            "total_asset": 10000,
            "fixed_expenditure": 3000,
            "persona": persona_dictionary[0]
        },
    },

    "prompt_display": True,
    "response_display": True,
    "info_display": True,
}

if __name__ == "__main__":
    task_name = task_parameters['task']
    
    task_description = 'NoPersonaNoCommunication'

    task_parameters['output_path'] = task_parameters['output_path'].format(
        record_path = data_output.record_path(task_name, task_parameters['model'], task_description),
        record_name = data_output.record_name(task_name)
    )

    if task_name in ["0", "1", "2"]:
        task_parameters['n_players'] = 2
        task(task_parameters, api_key)
    elif task_name in ["3"]:
        task_parameters['n_players'] = 3
        task(task_parameters, api_key)
