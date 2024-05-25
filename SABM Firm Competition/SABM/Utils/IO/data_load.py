import pandas as pd

def load_data(task_parameters, firms, db):
    load_template = "./Output/{path}/{name}_{filetype}.csv"
    name = task_parameters['load_data_name'].rsplit('_', 1)[0].replace('Record_', '')
    
    df = pd.read_csv(load_template.format(path = task_parameters['load_data_name'], name = name, filetype = 'overview_seperate'))

    data_row = []

    for id in range(1, task_parameters['n_players'] + 1):
        data_row.append(df[df['Firm_ID'] == id])
    
    for id in range(1, task_parameters['n_players'] + 1):
        for fm in firms:
            if fm.id == id:
                fm.history['price_history'] = list(data_row[id - 1]['Price'].values)
                fm.history['demand_history'] = list(data_row[id - 1]['Demand'].values)
                fm.history['profit_history'] = list(data_row[id - 1]['Profit'].values)
                fm.history['asset_history'] = list(data_row[id - 1]['Asset'].values)
                fm.price = fm.history['price_history'][-1]
                fm.demand = fm.history['demand_history'][-1]
                fm.profit = fm.history['profit_history'][-1]
                fm.total_asset = fm.history['asset_history'][-1]
    
    round_length = len(firms[0].history['price_history'])
    for index in range(0, round_length):
        for fm in firms:
            db.decision_history[fm.id].append([fm.history['price_history'][index], fm.history['demand_history'][index], fm.history['profit_history'][index], fm.history['asset_history'][index]])
    
    df = pd.read_csv(load_template.format(path = task_parameters['load_data_name'], name = name, filetype = 'strategy'))

    data_row = []

    for id in range(1, task_parameters['n_players'] + 1):
        data_row.append(df[df['Firm_ID'] == id])

    for id in range(1, task_parameters['n_players'] + 1):
        for fm in firms:
            if fm.id == id:
                fm.strategy = list(data_row[id - 1]['Strategy'].values)
    
    task_parameters['start_round'] = round_length + 1

    return task_parameters, firms, db
