from importlib import resources
import pandas as pd 
import requests
from patient import new_patient
from condition import new_condition
from os.path import exists

def test():
    r1 = 'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json'
    r2 = 'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Aaron697_Jerde200_6fa23508-960e-ff22-c3d0-0519a036543b.json'
    r3 =  'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Abbey813_Price929_83524678-9bff-93b7-ef89-d7f5390072ff.json'
    r4 = 'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Beth967_Hansen121_4e343b0a-8698-b6dd-64c6-c2d2d0959e6e.json'
    url = r4
    read_data(url)

#Get data from url
def read_data(url):
    try:
        data = requests.get(url)     
        data = data.json()        
        for counter, i in enumerate(data['entry']):
            resource = i['resource']['resourceType']
        
            if resource == 'Patient':
                patient = create_patient(data, counter)
                if exists('csv_files/patient.csv') == False: 
                    df = pd.DataFrame.from_dict([patient])
                    df.to_csv('csv_files/patient.csv')
                else:
                    df = pd.read_csv('csv_files/patient.csv')
                    df_newRecord = pd.DataFrame.from_dict([patient])
                    df = df.append(df_newRecord, ignore_index = True)
                    #drop indentical patient records
                    df = df.drop_duplicates()
                    #overwrite Csv file
                    df.to_csv('csv_files/patient.csv')              
            if resource == 'Condition':
                #condition = create_condition(data,counter)
                pass
            if resource == 'Claim':
                pass
            if resource == 'DiagnosticReport':
                pass
            if resource == 'Encounter':
                pass
    except Exception as error: 
        print(f'Data could not be loaded {error}')
          

def create_patient(data,counter):    
    pt = new_patient(data['entry'][counter]['resource'])
    return(pt.merge_record())

def create_condition(data, counter):
    condition_record = new_condition(data['entry'][counter]['resource'])
    return condition_record.condition







test()
