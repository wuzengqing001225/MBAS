from workflow_devaluation_beta import task
from SABM.Utils.IO import data_output

api_key = "sk-"

task_parameters = {
    # Model
    "model": 'gpt-4-0125-preview',
    "max_tokens": 128,

    "record_path": "{record_path}",
    "record_name": "{record_name}",

    # Load Data
    "load_data": False,
    "load_data_name": "",

    # Command Set for Prompt
    "order_set": ['task', 'role', 'history', 'action', 'output', 'rule'],

    # Simulation Loop
    "loop_max": 3,
    "loop_breakpoint": 1,
    "history_range": 20,
    "start_round": 1,

    # Task Specific Parameters
    ## Task
    "task": "0",

    ## Number of Agents
    "n_agents": 6,
    "f_ratio": 0.5,
    
    ## Properties of Agents (-1: None, 0: Even Distribution, 1: Real World Distribution)
    "properties_agents": {
        "p_education": 1,
        "p_race": -1,
        "p_personalities": -1,
    },

    "n_jobs": 2,
    "job_initial_distribution": 0,

    ## Communication
    "communication": False,
    "communication_rounds": 1,

    # Display
    "prompt_display": True,
    "response_display": True,
    "info_display": True,
}

if __name__ == "__main__":
    task_name = task_parameters['task']
    task_description = ""

    #task_parameters['record_path'] = data_output.record_path(task_name, task_parameters['model'], task_description),
    #task_parameters['record_name'] = data_output.record_name(task_name)

    if task_name in ["0"]:
        #task_parameters['properties_agents'] = {key: -1 for key in task_parameters['properties_agents']}
        task(task_parameters, api_key)
