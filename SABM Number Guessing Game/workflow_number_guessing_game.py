from SABM.Class.adjudicator import adjudicator
from SABM.Class.guesser import guesser
from SABM.Utils.Implement_Tools import display

def task_default(task_parameters, api_key = ''):
    # Definition of Agents
    adjudicator_instance = adjudicator(id = 1, model = task_parameters['model'], api_key = api_key)
    guesser_instance = guesser(id = 2, model = task_parameters['model'], api_key = api_key)

    # First Round
    target_number = adjudicator_instance.adjudicator_first_round(task_parameters)
    guess = guesser_instance.guesser_first_round(task_parameters)
    info_to_adjudicator = {'guess': guess}

    if task_parameters["info_display"]: display.display_variables('Target', target_number)

    # Main Loop
    loop_round = 1
    loop_max = task_parameters["loop_max"]

    while loop_round < loop_max:
        # Judge [Adjudicator]
        judgment = adjudicator_instance.adjudicator_continue(task_parameters, info_to_adjudicator)
        info_to_guesser = {'judgment': judgment}
        
        # Exit Condition Success
        if 'congratulations' in judgment.lower():
            display.display_results(0)
            break

        # Guess [Guesser]
        loop_round += 1
        guess = guesser_instance.guesser_continue(task_parameters, info_to_guesser)
        info_to_adjudicator = {'guess': guess}

    # Exit Condition Fail
    if loop_round == loop_max:
        display.display_results(-1)

    # Analysis
    key_indicator = {
        'task': {
            'target_number': target_number,
        },
        'round': [loop_round, "Guess History", guesser_instance.guess_history],
    }
    display.display_results_timeseries(key_indicator)
