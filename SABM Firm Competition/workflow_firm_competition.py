from SABM.Class.firm import firm
from SABM.Class.database import database
from SABM.Utils.Implement_Tools import display
from SABM.Utils.IO import data_load
from SABM.Utils.IO import data_output
from SABM.Utils.Visualization import plot
from SABM.Class import theoretical_rules
import matplotlib.pyplot as plt
import random

def task(task_parameters, api_key = ''):
    # Definition of Agents
    N = task_parameters['n_players']
    firms = []
    for i in range(1, N + 1):
        firms.append(firm(id = i, firm_name = task_parameters['firm_parameter'][i]['name'],
                 cost = task_parameters['firm_parameter'][i]['cost'],
                 a = task_parameters['firm_parameter'][i]['a'],
                 d = task_parameters['firm_parameter'][i]['d'],
                 beta = task_parameters['firm_parameter'][i]['beta'],
                 total_asset = task_parameters['firm_parameter'][i]['total_asset'],
                 fixed_expenditure = task_parameters['firm_parameter'][i]['fixed_expenditure'],
                 persona = task_parameters['firm_parameter'][i]['persona'],
                 model = task_parameters['model'], api_key = api_key, max_tokens = task_parameters['max_tokens']))
    
    db = database(firms)
    theoretical_rules.theoretical_profit(firms, db)

    # Environment Settings
    output_path = task_parameters['output_path']
    data_output.initialize(output_path, N)
    plt.ion()

    # Initialize Prompts
    for fm in firms:
        fm.init_command(task_parameters)
    if task_parameters["info_display"]:
        display.display(firms[0], display.display_prompt(firms[0].command, task_parameters['order_set']), 'info', 'prompt template')
        
    # Load Data
    if task_parameters['load_data']:
        task_parameters, firms, db = data_load.load_data(task_parameters, firms, db)
        plot.fig_output(output_path, db)
    
    #return # Check the prompts
    
    # Main Loop
    loop_max = task_parameters["loop_max"]
    loop_breakpoint = task_parameters["loop_breakpoint"]
    start_round = task_parameters['start_round']

    for loop_round in range(start_round, loop_max):
        # Break every loop_breakpoint rounds
        if task_parameters["info_display"]: display.display_round(loop_round)
        if display.breakpoint(loop_round, loop_breakpoint):
            data_output.data_text_output(output_path, 'overview', db, N)
            data_output.data_text_output(output_path, 'overview_seperate', db, N)
            data_output.data_text_output(output_path, 'conversation', db, N, start_round)
            data_output.data_text_output(output_path, 'strategy', db, N)
            plot.fig_output(output_path, db)
            break
        tm_flag = False # Terminate flag
        
        # Reorder firms
        random.shuffle(firms)
        
        for fm in firms:
            info = {'loop_round': loop_round}
            background_prompt = fm.background_prompt(task_parameters, db)
            decision_history = fm.historical_decisions(task_parameters, info, db)
            fm.context_prompt = background_prompt + decision_history
            
        # Phase 1: Communication between firms
        if task_parameters['communication']:
            if task_parameters["info_display"]: display.display_phase(loop_round, 'communication')
            for communication_round in range(task_parameters['communication_rounds']):
                for fm in firms:
                    info = {'loop_round': loop_round, 'communication_context': db.round_communication_context}
                    response = fm.firm_communication(task_parameters, info)
                    db.round_communication_context += response
        
        # Phase 2: Price decision
        if task_parameters["info_display"]: display.display_phase(loop_round, 'decision')

        for fm in firms:
            ## 2-1 Strategy making every history_range rounds
            history_range = task_parameters['history_range']
            if loop_round >= history_range and loop_round % history_range == 1:
                info = {'loop_round': loop_round, 'communication_context': db.round_communication_context}
                fm.generate_strategy(task_parameters, info)
            
            ## 2-2 Price decision            
            info = {'loop_round': loop_round, 'communication_context': db.round_communication_context}

            if loop_round == 1 and task_parameters['set_initial_price'] == True:
                fm.price = task_parameters['initial_price'][fm.id]
                fm.history['price_history'].append(fm.price)
            else:
                fm.choice_price(task_parameters, info)
            
        # Phase 3: Accounting and observation
        if task_parameters["info_display"]: display.display_phase(loop_round, 'accounting')
        info = {'loop_round': loop_round}
        for fm in firms:
            fm.calc_demand(db)
            fm.calc_profit(info)
            fm.calc_asset()
            db.decision_history[fm.id].append([fm.price, fm.demand, fm.profit, fm.total_asset])
        
        # Data processing
        db.communication_context.append(db.round_communication_context)
        db.round_communication_context = ""
        for fm in firms:
            fm.context_prompt = ""

        plot.visulization(output_path, db)

        ## Save data every 10 rounds
        if loop_round % 10 == 0:
            data_output.data_text_output(output_path, 'overview', db, N)
            data_output.data_text_output(output_path, 'overview_seperate', db, N)
            data_output.data_text_output(output_path, 'conversation', db, N)
            data_output.data_text_output(output_path, 'strategy', db, N)
            if loop_round % 100 == 0:
                plot.fig_output(output_path, db)
        
        # Terminate Condition
        for fm in firms:
            if fm.total_asset <= 0:
                if task_parameters["info_display"]: display.display_results(1)
                data_output.data_text_output(output_path, 'overview', db, N)
                data_output.data_text_output(output_path, 'overview_seperate', db, N)
                data_output.data_text_output(output_path, 'conversation', db, N)
                data_output.data_text_output(output_path, 'strategy', db, N)
                plot.fig_output(output_path, db)
                tm_flag = True
        if tm_flag: break

    plt.close()
    if task_parameters["info_display"]: display.display_results(0)
