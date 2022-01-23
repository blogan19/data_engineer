import pandas as pd 
import requests
from patient import new_patient

def test():
    pt1 = 'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json'
    pt2 =  'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Abbey813_Price929_83524678-9bff-93b7-ef89-d7f5390072ff.json'
    pt3 = ''
    url = pt2
    read_data(url)

#Get data from url
def read_data(url):
    data = requests.get(url)     
    data = data.json()
    #df = pd.DataFrame([patient_record])
    #print(df)
    print(create_patient(data))


def create_patient(data):    
    for i in data['entry']:
        record = i['resource']['resourceType']
        if record == 'Patient':
            pt = new_patient(i['resource'])
            return(pt.merge_record())
        else:
            print(f'No patient record found')
test()
