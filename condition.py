from fhir.resources.condition import Condition
import json
from datetime import datetime 


class new_condition:
    def __init__(self, record):
        self.condition = self.get_condition(record)

    def get_condition(self,pt_record):
       # print(f'Patient record created: \n {json.dumps(pt_record, indent=4, sort_keys=True)}')
        c = Condition.parse_obj(pt_record)

        pt_condition = {
            "clinicalStatus": c.clinicalStatus.text,
            "verificationStatus": c.verificationStatus.text,
            "category": c.category[0].coding[0].display,
            "severity": c.severity,
            "code": c.code.coding[0].display,
            "bodySite": c.bodySite,
            "subject": c.subject.display,
            "encounter": c.encounter.display,
            "onsetDateTime": c.onsetDateTime,
            "onsetAge": c.onsetAge,
            "onsetPeriod" : c.onsetPeriod,
            "onsetRange" : c.onsetRange,
            "onsetString" : c.onsetString,
            "abatementDateTime" : c.abatementDateTime,
            "abatementAge" : c.abatementAge,
            "abatementPeriod" : c.abatementPeriod,
            "abatementRange" : c.abatementRange,
            "abatementString": c.abatementString,
            "recordedDate": c.recordedDate,
            "recorder": c.recorder,
            "asserter": c.asserter,
            "stage": c.stage,
            "evidence": c.evidence,
            "note": c.note
        }

        #clean_dates
        def date_clean(date_type):
            #if date is present then reformat it 
            try:
                date_val = pt_condition.get(date_type)
                if date_val != None:
                    pt_condition[date_type] = date_val.strftime("%c") 
            except Exception: 
                pass

        date_clean('onsetDateTime')  
        date_clean('abatementDateTime')
        date_clean('recordedDate')

        return pt_condition
        