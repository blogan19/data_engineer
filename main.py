from importlib import resources
import pandas as pd 
import requests
from patient import new_patient
from condition import new_condition

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
                print(patient)                
            if resource == 'Condition':
                pass
                #condition = create_condition(data,counter)
                #print(condition)
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
