import fhir.resources
import pandas as pd 
import requests

def test():
    pt1 = 'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json'
    pt2 =  'https://raw.githubusercontent.com/emisgroup/exa-data-eng-assessment/main/data/Abbey813_Price929_83524678-9bff-93b7-ef89-d7f5390072ff.json'
    url = pt2
    read_data(url)

#Get data from url
def read_data(url):
    x = requests.get(url)     
    x= x.json()
    pt = create_patient(x)
    pt_extensions = extensions(x)
    print(pt)
    print(pt_extensions)





def create_patient(x):
    pt_entry = x['entry']
    pt_entry = pt_entry[0]['resource']
    if pt_entry['resourceType'] == 'Patient':
        pt_record = {
            'id':pt_entry['id'],
            'title': pt_entry['name'][0]['prefix'][0],
            'family_name': pt_entry['name'][0]['family'],
            'given_name': pt_entry['name'][0]['given'][0],
            'phone_number': pt_entry['telecom'][0]['value'],
            'phone_type': pt_entry['telecom'][0]['use'],
            'gender': pt_entry['gender'],
            'birth_date': pt_entry['birthDate'],
            'date_of_death': pt_entry.get('deceasedDateTime'),
            'address': pt_entry['address'][0]['line'][0],
            'city': pt_entry['address'][0]['city'],
            'state': pt_entry['address'][0]['state'],
            'country': pt_entry['address'][0]['country'],
            'marital': pt_entry['maritalStatus']['coding'][0]['code'],
            'multipleBirth': pt_entry['multipleBirthBoolean'],
            'communication': pt_entry['communication'][0]['language']['coding'][0]['code']
        }
        df = pd.DataFrame([pt_record])
        return pt_record 

def extensions(x):
    pt_entry = x['entry'][0]['resource']

    url_reference = {
        'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race': ('us_core_race',pt_entry['extension'][0]['extension'][0]['valueCoding']['display']),
        'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity': ('us_core_ethnicity',pt_entry['extension'][1]['extension'][0]['valueCoding']['display']),
        'http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName': ('mothers_maiden',pt_entry['extension'][2]['valueString']),
        'http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex':('us_core_birthsex', pt_entry['extension'][3]['valueCode']),
        'http://hl7.org/fhir/StructureDefinition/patient-birthPlace':('birth_place',pt_entry['extension'][4]['valueAddress']),
        'http://synthetichealth.github.io/synthea/disability-adjusted-life-years':('disability_adj_life_years',pt_entry['extension'][5]['valueDecimal']),
        'http://synthetichealth.github.io/synthea/quality-adjusted-life-years':('quality_adj_life_years',pt_entry['extension'][6]['valueDecimal'])
    }
    pt_extensions = {}
    #Loops of url references. If matching url adds relevant data to pt_extension dict
    for i in pt_entry['extension']:
        if i['url'] in url_reference:
            # get tuple from reference dict
            ext_item = url_reference[i['url']]
            #create extension dictionary key value pairs
            pt_extensions[ext_item[0]] = ext_item[1]
    return pt_extensions





test()
