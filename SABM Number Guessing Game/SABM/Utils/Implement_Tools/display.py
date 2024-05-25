def display(agent, prompt:str, type:str):
    if type == 'i':
        print(f"<<PROMPT>> To Agent {agent.id} [{agent.type}]\n{prompt}\n")
    elif type == 'o':
        print(f"<<RESPONSE>> Agent {agent.id} [{agent.type}]:\n{prompt}\n")

def display_error(message:str, position = '', type = 'default'):
    if type == 'default':
        if position == '':
            print(f'[Error] {message}')
        else:
            print(f'[Error] {message} @ {position}')
    else:
        print(f'[{type} Error] {message} @ {position}')

def display_results(return_value = 0):
    if return_value == 0:
        print('Simulation Completed (Guesser found target number)')
    if return_value == -1:
        print('Simulation Completed (Guesser failed)')

def display_variables(var_name, var, round = 0, display_round = False):
    if display_round == False:
        print(f'{var_name}: {var}')
    else:
        print(f'#{round}: {var_name}: {var}')

def display_round(round = 0):
    print(f'#{round}\n')

def display_results_timeseries(key_indicator:dict):
    print("\n=================")
    if 'task' in key_indicator.keys():
        print("# Task")
        for k, v in key_indicator['task'].items():
            print(f"{k}: {v}")
        print()
    if 'round' in key_indicator.keys():
        print(f"# Round: {key_indicator['round'][0]}")
        if len(key_indicator['round']) > 1:
            for item_index in range(1, len(key_indicator['round']), 2):
                print(f"{key_indicator['round'][item_index]}: ")
                for i in key_indicator['round'][item_index + 1]:
                    print(i, end = ' ')
                print()
