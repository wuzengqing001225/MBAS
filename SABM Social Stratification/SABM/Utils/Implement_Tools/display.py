from SABM.Utils.Text_Processing import format_prompt

def display(agent, prompt:str, type:str, context:str = ''):
    if context == '':
        if type == 'i':
            print(f"<<PROMPT>> To Agent {agent.id} [{agent.type.capitalize()}]\n{prompt}\n")
        elif type == 'o':
            print(f"<<RESPONSE>> Agent {agent.id} [{agent.type.capitalize()}]:\n{prompt}\n")
    else:
        if type == 'i':
            print(f"<<PROMPT ({context.capitalize()})>> To Agent {agent.id} [{agent.type.capitalize()}]\n{prompt}\n")
        elif type == 'o':
            print(f"<<RESPONSE ({context.capitalize()})>> Agent {agent.id} [{agent.type.capitalize()}]:\n{prompt}\n")
        elif type == 'info':
            print(f"<<INFO>> Agent {agent.id} {context.capitalize()}:\n{prompt}")

def display_prompt(prompt_dictionary, order_set):
    display_info = ""
    for k, v in prompt_dictionary.items():
        prompt = {
            "command": v,
            "value": {}
        }
        display_info += f'=== {k.capitalize()} ===\n\n{format_prompt.link_prompt(prompt, order_set)}\n\n'
    return display_info + '\n'

def display_dict(dict, type = "Var"):
    display_info = ""
    for k, v in dict.items():
        display_info += f"<<{type}>> {k}\n{v}\n"
    print(display_info)

def display_error(message:str, position = '', type = 'default'):
    if type == 'default':
        if position == '':
            print(f'[Error] {message}')
        else:
            print(f'[Error] {message} @ {position}')
    else:
        type = type.capitalize()
        print(f'[{type} Error] {message} @ {position}')

def display_results(return_value = 0, message = ""):
    if return_value == 0:
        print('Simulation Completed')
    if return_value == 1:
        print(f'Simulation Completed ({message})')

def display_variables(var_name, var, round = 0, display_round = False):
    if display_round == False:
        print(f'{var_name}: {var}')
    else:
        print(f'#{round}: {var_name}: {var}')

def display_round(round = 0):
    print(f'# Round #{round}\n')

def display_phase(round = 0, phase = ''):
    if 'a' < phase[0] < 'z': phase = phase.capitalize()
    print(f'=== {phase} Phase (Round #{round}) ===\n')

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

def breakpoint(round, loop_breakpoint):
    if round != 0:
        if (round + 1) % loop_breakpoint == 0:
            breakpoint_key = str(input("Continue? (Y/N) "))
            if breakpoint_key[0] == 'N' or breakpoint_key[0] == 'n':
                return True
    return False

def round_function(x: float, deci = 2):
    return round(x, deci)