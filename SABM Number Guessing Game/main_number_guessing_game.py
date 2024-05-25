from workflow_number_guessing_game import task_default

api_key = "sk-"

task_parameters = {
    "model": 'gpt-4-0314',

    "order_set": ['task', 'role', 'history', 'action', 'output'],
    "loop_max": 50,
    "range_begin": 1,
    "range_end": 100,

    "prompt_display": True,
    "response_display": True,
    "info_display": True,
}

task_default(task_parameters, api_key)