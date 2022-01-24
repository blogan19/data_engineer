import pandas as pd 
import requests
from patient import new_patient
import json

def test():
    r1 = 'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json'
    r2 = 'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Aaron697_Jerde200_6fa23508-960e-ff22-c3d0-0519a036543b.json'
    r3 =  'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Abbey813_Price929_83524678-9bff-93b7-ef89-d7f5390072ff.json'
    r4 = 'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Beth967_Hansen121_4e343b0a-8698-b6dd-64c6-c2d2d0959e6e.json'
    url = r2
    read_data(url)

#Get data from url
def read_data(url):
    try:
        data = requests.get(url)     
        data = data.json()
        patient_record = create_patient(data)
        print(f'Patient record created: \n {json.dumps(patient_record, indent=4, sort_keys=True)}')
        
        #df = pd.DataFrame([patient_record])
        #print(df)

    except Exception as error: 
        print(f'Data could not be loaded {error}')

def create_patient(data):    
    for i in data['entry']:
        record = i['resource']['resourceType']
        if record == 'Patient':
            pt = new_patient(i['resource'])
            return(pt.merge_record())
        else:
            print(f'No patient record found')
test()
