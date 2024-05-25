def numerical_history(data, type = 'simple_round', sep = ',', label = ''):
    history = ""
    for index in range(len(data)):
        if type == 'round':
            history += f'Round {index + 1}: {data[index]}\n'
        elif type == 'simple_round':
            history += f'{data[index]}'
            if index != len(data) - 1: history += sep + ' '
    return history
