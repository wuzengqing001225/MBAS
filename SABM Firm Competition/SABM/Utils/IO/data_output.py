import csv
import datetime
import time
import os

def record_path(task, model_ver, memo = ''):
    if "gpt-4" in model_ver: model_ver = "GPT4"
    else: model_ver = "GPT3.5"

    output_path = f"./Output/Task_{task}_Record_{datetime.date.today().strftime('%y%m%d')}_{time.strftime('%H%M')}_{model_ver}"
    if memo != '': output_path += f'{memo}'
    
    os.makedirs(output_path, exist_ok=True)

    return output_path

def record_name(task):
    return f"Task_{task}_{datetime.date.today().strftime('%y%m%d')}_{time.strftime('%H%M')}"

def initialize(csv_filepath:str, n_players:int):
    filename_format = "{csv_filepath}_{type}.csv"

    with open(filename_format.format(csv_filepath = csv_filepath, type = "conversation"), mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['Round', 'Conversation']
        writer.writerow(header)
    
    with open(filename_format.format(csv_filepath = csv_filepath, type = "overview"), mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['Round']
        for i in range(n_players):
            header.append(f'Price {i + 1}')
            header.append(f'Demand {i + 1}')
            header.append(f'Profit {i + 1}')
            header.append(f'Asset {i + 1}')
        writer.writerow(header)
    
    with open(filename_format.format(csv_filepath = csv_filepath, type = "overview_seperate"), mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['Round', 'Firm_ID', 'Price', 'Demand', 'Profit', 'Asset']
        writer.writerow(header)

    with open(filename_format.format(csv_filepath = csv_filepath, type = "strategy"), mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['Round', 'Firm_ID', 'Strategy']
        writer.writerow(header)


def data_text_output(csv_filepath:str, type:str, data, n_players:int, start_round = 1):
    filename_format = "{csv_filepath}_{type}.csv"
        
    with open(filename_format.format(csv_filepath = csv_filepath, type = type), mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        if type == 'conversation':
            header = ['Round', 'Conversation']
            writer.writerow(header)
            for d_index in range(len(data.communication_context)):
                writer.writerow([d_index + start_round, data.communication_context[d_index]])
        
        if type == 'strategy':
            header = ['Firm_ID', 'Strategy']
            writer.writerow(header)
            for fm in data.firms:
                for st in fm.strategy:
                    writer.writerow([fm.id, st])

        if type == 'overview':
            header = ['Round']
            for i in range(n_players):
                header.append(f'Price {i + 1}')
                header.append(f'Demand {i + 1}')
                header.append(f'Profit {i + 1}')
                header.append(f'Asset {i + 1}')
            writer.writerow(header)

            for i in range(len(data.decision_history[1])):
                row = []
                row.append(i + 1)

                for id in range(1, n_players + 1):
                    for item in range(4):
                        row.append(data.decision_history[id][i][item])
                
                writer.writerow(row)
        
        if type == 'overview_seperate':
            header = ['Round', 'Firm_ID', 'Price', 'Demand', 'Profit', 'Asset']
            writer.writerow(header)

            for i in range(len(data.decision_history[1])):
                for id in range(1, n_players + 1):
                    row = []
                    row.append(i + 1)
                    row.append(id)
                    for item in range(4):
                        row.append(data.decision_history[id][i][item])
                    writer.writerow(row)