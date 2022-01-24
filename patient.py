from fhir.resources.patient import Patient
from fhir.resources.identifier import Identifier



class new_patient:
    def __init__(self,record):
        self.pt_details = pt_details(record)
        self.pt_identifiers = pt_identifiers(record)
        self.pt_details = pt_details(record)
        
    def merge_record(self): 
        #merges the three dictionaries
        p = self.pt_details | self.pt_identifiers | self.pt_details
        return p

def pt_details(pt_entry): 
    #Call key check function
    key_check = check_keys(pt_entry.keys())
    
    # add expected keys to pt_record dictionary
    pt_record = {
        'id':pt_entry['id'],
        'title': pt_entry['name'][0]['prefix'][0],
        'family_name': pt_entry['name'][0]['family'],
        'given_name': pt_entry['name'][0]['given'][0],
        'phone_number': pt_entry['telecom'][0]['value'],
        'phone_type': pt_entry['telecom'][0]['use'],
        'gender': pt_entry.get('gender'),
        'birth_date': pt_entry.get('birthDate'),
        'date_of_death': pt_entry.get('deceasedDateTime'),
        'address': pt_entry['address'][0]['line'][0],
        'city': pt_entry['address'][0]['city'],
        'state': pt_entry['address'][0]['state'],
        'country': pt_entry['address'][0]['country'],
        'marital': pt_entry['maritalStatus']['coding'][0]['code'],
        'multipleBirth': pt_entry.get('multipleBirthBoolean'),
        'communication': pt_entry['communication'][0]['language']['coding'][0]['code']
    }
    #If a key is not part of the expected keys dictionary add it to the dictionary
    if len(key_check) > 0:
        for i in key_check:
            pt_record[i] = pt_entry[i]
            print(f'Key added: {pt_record[i]}')
    return pt_record 

def check_keys(key_list):
        expected_keys = ['resourceType', 'id', 'meta', 'text', 'extension', 'identifier', 'name', 'telecom', 'gender', 'birthDate', 'deceasedDateTime', 'address', 'maritalStatus', 'multipleBirthBoolean', 'communication']
        err = []
        for i in key_list:
            if i not in expected_keys:
                err.append(i)
                print(f'{i} not in keys')
        return err


def pt_identifiers(patient):
    identifiers = {}
    #validate identifiers 
    p = Patient.parse_obj(patient)
    validate = isinstance(p.identifier[0],Identifier)

    if validate == True:
        for i in patient['identifier']:
            if i.get('type') != None:
                identifiers[i['type']['text']] = i['value']
        return(identifiers)
    
def pt_extensions(pt_entry):
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
    #Loops url references. If matching url adds relevant data to pt_extension dict
    for i in pt_entry['extension']:
        if i['url'] in url_reference:
            # get tuple from reference dict
            ext_item = url_reference[i['url']]
            
            #if field is a dictionary the fields within are concatenated
            if type(ext_item[1]) is dict:
                pt_extensions[ext_item[0]] = ' '.join(ext_item[1].values())
            else:
                pt_extensions[ext_item[0]] = ext_item[1]
    return pt_extensions

