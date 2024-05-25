import csv
import datetime
import time
import os

def record_path(task, model_ver, memo = ''):
    if "gpt-4" in model_ver:
        if "preview" in model_ver:
            model_ver = "GPT4-Turbo"
        else:
            model_ver = "GPT4"
    else: model_ver = "GPT3.5"

    output_path = f"./Output/Task_{task}_Record_{datetime.date.today().strftime('%y%m%d')}_{time.strftime('%H%M')}_{model_ver}"
    if memo != '': output_path += f'{memo}'
    
    os.makedirs(output_path, exist_ok=True)

    return output_path

def record_name(task):
    return f"Task_{task}_{datetime.date.today().strftime('%y%m%d')}_{time.strftime('%H%M')}"

def initialize(csv_filepath:str):
    with open("", mode='w', newline='') as csv_file:
        pass
