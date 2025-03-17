from .utils import format_address_item, format_none_to_null_string

class PatientData():
    __slots__=[
        "nhs_number",
        "name",
        "address",
        "dob",
        "gender"
        ]
    
    def __init__(self, patient_resource=None):
        self.nhs_number=patient_resource.identifier[0].value # assumes NHS number is first identifier
        
        name_item=patient_resource.name[0] # just taking the first of available full names
        self.name=format_none_to_null_string(name_item.family)
        if name_item.given:
            for given in name_item.given:
                self.name+=", "+given

        self.address=format_address_item(address_item=patient_resource.address[0]) # just taking first of available addresses  
        self.dob=format_none_to_null_string(patient_resource.birthDate)
        self.gender=format_none_to_null_string(patient_resource.gender)