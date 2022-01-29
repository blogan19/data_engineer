from fhir.resources.patient import Patient
from fhir.resources.identifier import Identifier
from fhir.resources.humanname import HumanName
from fhir.resources.address import Address
from fhir.resources.extension import Extension

class new_patient:
    def __init__(self,record):
        self.pt_details = pt_details(record)
        self.pt_extensions = pt_extensions(record)
        
    def merge_record(self): 
        #merges the three dictionaries
        p = self.pt_details | self.pt_extensions
        return p

def pt_details(patient): 
    #Call key check function
    #key_check = check_keys(pt_entry.keys())
    p = Patient.parse_obj(patient)

    pt_record = {
        'id':p.id,
        'active':p.active,
        'title': p.name[0].prefix[0],
        'given_name': p.name[0].given[0],
        'family_name': p.name[0].family[0],
        'family_name': patient['name'][0]['family'],
        'given_name': patient['name'][0]['given'][0],
        'phone_number': p.telecom[0].value,
        'phone_type': p.telecom[0].use,
        'gender': p.gender,
        'birth_date': p.birthDate,
        'deceased_boolean': p.deceasedBoolean,
        'deceased_date': p.deceasedDateTime,
        'address': p.address[0].line[0],
        'city': p.address[0].city,
        'state': p.address[0].state,
        'country': p.address[0].country,
        'marital': p.maritalStatus.coding[0].display,
        'multipleBirth': p.multipleBirthBoolean,
        'multipleBirthInteger': p.multipleBirthInteger,
        "photo": p.photo,
        "contact": p.contact,
        'communication': p.communication[0].language.coding[0].code,
        'preferred': p.communication[0].preferred,
        'generalPractitioner': p.generalPractitioner,
        'managingOrganization': p.managingOrganization,
        'medical_record_number': p.identifier[1].value,
        'social_security_number':p.identifier[2].value,
        'driving_license':p.identifier[3].value,
        'passport_number': p.identifier[4].value
    }
    return pt_record
    
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

