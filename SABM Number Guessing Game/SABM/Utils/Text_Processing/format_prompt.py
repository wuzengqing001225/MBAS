from SABM.Prompt.prompt import task_prompt

def link_prompt(prompt:str, order_set:list, sep = ','):
    # maximum 3 parameters following one order
    formatted_prompt = ""
    pt = prompt["command"].replace(sep, '')
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
                    formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                    formatted_prompt += ' '
                else:
                    dict_prompt = ''
                    for v in prompt_key[key].values():
                        dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                    formatted_prompt += dict_prompt
            else:
                key = f"{order[seme_index]}"
                if type(prompt_key[key]) != dict:
                    formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                    formatted_prompt += ' '
                else:
                    dict_prompt = ''
                    for v in prompt_key[key].values():
                        dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                    formatted_prompt += dict_prompt
            
            seme_index = seme_index + 1
        
        # 1 Parameter
        elif seme_index + 2 == len_order or order[seme_index + 2] in order_set:
            if order[seme_index + 1][0] != '-':
                key = f"{order[seme_index]}_{order[seme_index + 1]}"
                if type(prompt_key[key]) != dict:
                    formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                    formatted_prompt += ' '
                else:
                    dict_prompt = ''
                    for v in prompt_key[key].values():
                        dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                    formatted_prompt += dict_prompt
            else:
                if f"{order[seme_index]}_default" in prompt_key.keys():
                    key = f"{order[seme_index]}_default"
                    if type(prompt_key[key]) != dict:
                        formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                        formatted_prompt += ' '
                    else:
                        dict_prompt = ''
                        for v in prompt_key[key].values():
                            dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                        formatted_prompt += dict_prompt
                else:
                    key = f"{order[seme_index]}"
                    if type(prompt_key[key]) != dict:
                        formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                        formatted_prompt += ' '
                    else:
                        dict_prompt = ''
                        for v in prompt_key[key].values():
                            dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                        formatted_prompt += dict_prompt
                
                if order[seme_index + 1] == '-newline':
                    formatted_prompt += '\n'
                elif order[seme_index + 1] == '-tab':
                    formatted_prompt += '\t'
            
            seme_index = seme_index + 2
        
        # 2 Parameter
        elif seme_index + 3 == len_order or order[seme_index + 3] in order_set:
            if order[seme_index + 2][0] != '-':
                key = f"{order[seme_index]}_{order[seme_index + 1]}_{order[seme_index + 2]}" 
                if type(prompt_key[key]) != dict:
                        formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                        formatted_prompt += ' '
                else:
                    dict_prompt = ''
                    for v in prompt_key[key].values():
                        dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                    formatted_prompt += dict_prompt
            
            else:
                key = f"{order[seme_index]}_{order[seme_index + 1]}"
                if type(prompt_key[key]) != dict:
                        formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                        formatted_prompt += ' '
                else:
                    dict_prompt = ''
                    for v in prompt_key[key].values():
                        dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                    formatted_prompt += dict_prompt

                if order[seme_index + 2] == '-newline':
                    formatted_prompt += '\n'
                elif order[seme_index + 2] == '-tab':
                    formatted_prompt += '\t'
                
            seme_index = seme_index + 3
        
        # Space Parameter
        elif seme_index + 4 == len_order or order[seme_index + 4] in order_set:
            key = f"{order[seme_index]}_{order[seme_index + 1]}_{order[seme_index + 2]}"
            if type(prompt_key[key]) != dict:
                        formatted_prompt += prompt_key[key].format(**vl[order[seme_index]])
                        formatted_prompt += ' '
            else:
                dict_prompt = ''
                for v in prompt_key[key].values():
                    dict_prompt += v.format(**vl[order[seme_index]]) + ' '
                formatted_prompt += dict_prompt

            if order[seme_index + 3][0] == '-':
                if order[seme_index + 3] == '-newline':
                    formatted_prompt += '\n'
                elif order[seme_index + 3] == '-tab':
                    formatted_prompt += '\t'
            seme_index = seme_index + 4
    
    return formatted_prompt
