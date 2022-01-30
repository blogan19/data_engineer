from importlib import resources
import pandas as pd 
import requests
from patient import new_patient
from condition import new_condition
from os.path import exists
from get_test_urls import get_patients

def test():
    url = get_patients()
    data = requests.get(url)     
    if data.status_code == 200:
        data = data.json()  
        read_data(data)
    else:
        test()     

#Get data from url
def read_data(data):
    try:
         
        for counter, i in enumerate(data['entry']):
            resource = i['resource']['resourceType']
        
            if resource == 'Patient':

                #Create patient
                patient = create_patient(data, counter)

                if exists('csv_files/patient.csv') == False: 
                    df = pd.DataFrame([patient])
                    df.to_csv('csv_files/patient.csv', index=False)
                else:
                    df = pd.read_csv('csv_files/patient.csv')
                    
                    #check to see if record already exists
                    pt_id = patient['id']
                    index = df.index[df['id'] == pt_id].tolist()                                       
                    df_newRecord = pd.DataFrame.from_records([patient])

                    if len(index) > 0: 
                        df.loc[index] = df_newRecord
                    else:                     
                        df = df.append(df_newRecord,ignore_index=True)
                    
                    #drop indentical patient records
                    df = df.drop_duplicates()

                    #overwrite Csv file
                    df.to_csv('csv_files/patient.csv', index=False)    

            if resource == 'Condition':
                
                condition = create_condition(data,counter)
                if exists('csv_files/condition.csv') == False: 
                    df = pd.DataFrame([condition])
                    df.to_csv('csv_files/condition.csv', index=False)
                else: 
                    df = pd.read_csv('csv_files/condition.csv')
                    df_newRecord = pd.DataFrame.from_records([condition])

                    df = df.append(df_newRecord,ignore_index=True)

                    #overwrite Csv file
                    df.to_csv('csv_files/condition.csv', index=False)

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
