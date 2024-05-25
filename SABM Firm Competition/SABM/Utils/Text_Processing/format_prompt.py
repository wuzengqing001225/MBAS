from SABM.Prompt.prompt import task_prompt

def format_conversation(conversation):
    if conversation != "":
        return f"\n\nConversation so far:\n{conversation}"
    else:
        return ""

def format_strategy_1round(strategy):
    if len(strategy) > 0:
        return f"Your latest pricing strategy is: {strategy[-1]}\n"
    else:
        return ""

def format_strategy(strategy, history_range):
    previous_strategy = ""
    if len(strategy) > 0:
        previous_strategy += "Your strategy in previous rounds:\n"
        for strategy_id in range(max(0, len(strategy) - history_range), len(strategy)):
            previous_strategy += strategy[strategy_id] + '\n'
        return previous_strategy
    else:
        return ""

def format_other_firm_name(self_name, names, n_players):
    names = names[:n_players]
    names = [x for x in names if x != self_name]
    if len(names) == 1: return names[0]
    elif len(names) == 2: return f"{names[0]} and {names[1]}"
    else:
        formatted_prompt = ""
        for name_index in range(len(names)):
            if name_index <= len(names) - 3:
                formatted_prompt += names[name_index] + ', '
            elif name_index == len(names) - 2:
                formatted_prompt += names[name_index] + ', and '
            else:
                formatted_prompt += names[name_index]
        return formatted_prompt

def link_prompt(prompt:str, order_set:list, sep = ','):
    if '_' not in prompt["command"]:
        # maximum 3 parameters following one order
        formatted_prompt = ""
        pt = prompt["command"].lower().replace(sep, '')
        vl = prompt["value"]
        order = pt.split(' ')

        seme_index = 0
        len_order = len(order)

        while seme_index != len_order:
            prompt_key = task_prompt[order[seme_index]]

            # No Parameter
            if seme_index + 1 == len_order or order[seme_index + 1] in order_set:
                if f"{order[seme_index]}_default" in prompt_key.keys():
                    key = f"{order[seme_index]}_default"
                    if type(prompt_key[key]) != dict:
                        if len(vl) > 0:
                            formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                        else:
                            formatted_prompt += prompt_key[key]
                        formatted_prompt += ' '
                    else:
                        dict_prompt = ''
                        for v in prompt_key[key].values():
                            if len(vl) > 0:
                                dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                            else:
                                dict_prompt += v + ' '
                        formatted_prompt += dict_prompt
                else:
                    key = f"{order[seme_index]}"
                    if type(prompt_key[key]) != dict:
                        if len(vl) > 0:
                            formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                        else:
                            formatted_prompt += prompt_key[key]
                        formatted_prompt += ' '
                    else:
                        dict_prompt = ''
                        for v in prompt_key[key].values():
                            if len(vl) > 0:
                                dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                            else:
                                dict_prompt += v + ' '
                        formatted_prompt += dict_prompt
                
                seme_index = seme_index + 1
            
            # 1 Parameter
            elif seme_index + 2 == len_order or order[seme_index + 2] in order_set:
                if order[seme_index + 1][0] != '-':
                    key = f"{order[seme_index]}_{order[seme_index + 1]}"
                    if type(prompt_key[key]) != dict:
                        if len(vl) > 0:
                            formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                        else:
                            formatted_prompt += prompt_key[key]
                        formatted_prompt += ' '
                    else:
                        dict_prompt = ''
                        for v in prompt_key[key].values():
                            if len(vl) > 0:
                                dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                            else:
                                dict_prompt += v + ' '
                        formatted_prompt += dict_prompt
                else:
                    if f"{order[seme_index]}_default" in prompt_key.keys():
                        key = f"{order[seme_index]}_default"
                        if type(prompt_key[key]) != dict:
                            if len(vl) > 0:
                                formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                            else:
                                formatted_prompt += prompt_key[key]
                            formatted_prompt += ' '
                        else:
                            dict_prompt = ''
                            for v in prompt_key[key].values():
                                if len(vl) > 0:
                                    dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                                else:
                                    dict_prompt += v + ' '
                            formatted_prompt += dict_prompt
                    else:
                        key = f"{order[seme_index]}"
                        if type(prompt_key[key]) != dict:
                            if len(vl) > 0:
                                formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                            else:
                                formatted_prompt += prompt_key[key]
                            formatted_prompt += ' '
                        else:
                            dict_prompt = ''
                            for v in prompt_key[key].values():
                                if len(vl) > 0:
                                    dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                                else:
                                    dict_prompt += v + ' '
                            formatted_prompt += dict_prompt
                    
                    if order[seme_index + 1] == '-newline':
                        formatted_prompt += '\n'
                    elif order[seme_index + 1] == '-newline2':
                        formatted_prompt += '\n\n'
                    elif order[seme_index + 1] == '-tab':
                        formatted_prompt += '\t'
                
                seme_index = seme_index + 2
            
            # 2 Parameter
            elif seme_index + 3 == len_order or order[seme_index + 3] in order_set:
                if order[seme_index + 2][0] != '-':
                    key = f"{order[seme_index]}_{order[seme_index + 1]}_{order[seme_index + 2]}" 
                    if type(prompt_key[key]) != dict:
                            if len(vl) > 0:
                                formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                            else:
                                formatted_prompt += prompt_key[key]
                            formatted_prompt += ' '
                    else:
                        dict_prompt = ''
                        for v in prompt_key[key].values():
                            if len(vl) > 0:
                                dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                            else:
                                dict_prompt += v + ' '
                        formatted_prompt += dict_prompt
                
                else:
                    key = f"{order[seme_index]}_{order[seme_index + 1]}"
                    if type(prompt_key[key]) != dict:
                            if len(vl) > 0:
                                formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                            else:
                                formatted_prompt += prompt_key[key]
                            formatted_prompt += ' '
                    else:
                        dict_prompt = ''
                        for v in prompt_key[key].values():
                            if len(vl) > 0:
                                dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                            else:
                                dict_prompt += v + ' '
                        formatted_prompt += dict_prompt

                    if order[seme_index + 2] == '-newline':
                        formatted_prompt += '\n'
                    elif order[seme_index + 2] == '-newline2':
                        formatted_prompt += '\n\n'
                    elif order[seme_index + 2] == '-tab':
                        formatted_prompt += '\t'
                    
                seme_index = seme_index + 3
            
            # Space Parameter
            elif seme_index + 4 == len_order or order[seme_index + 4] in order_set:
                key = f"{order[seme_index]}_{order[seme_index + 1]}_{order[seme_index + 2]}"
                if type(prompt_key[key]) != dict:
                    if len(vl) > 0:
                        formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                    else:
                        formatted_prompt += prompt_key[key]
                    formatted_prompt += ' '
                else:
                    dict_prompt = ''
                    for v in prompt_key[key].values():
                        if len(vl) > 0:
                            dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                        else:
                            dict_prompt += v + ' '
                    formatted_prompt += dict_prompt

                if order[seme_index + 3][0] == '-':
                    if order[seme_index + 3] == '-newline':
                        formatted_prompt += '\n'
                    elif order[seme_index + 3] == '-newline2':
                        formatted_prompt += '\n\n'
                    elif order[seme_index + 3] == '-tab':
                        formatted_prompt += '\t'
                seme_index = seme_index + 4
        
        return formatted_prompt
    else:
        pass
