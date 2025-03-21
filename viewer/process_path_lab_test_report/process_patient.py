from .utils import format_address_item, format_None_to_null_string

class PatientData():
    __slots__=[
        "nhs_number",
        "name",
        "address",
        "dob",
        "gender"
        ]
    
    def __init__(self, patient_resource=None):
        if patient_resource.identifier is not None:
            self.nhs_number=format_None_to_null_string(patient_resource.identifier[0].value) # assumes NHS number is first identifier
        else:
            self.nhs_number=""
        
        if patient_resource.name is not None:
            name_item=patient_resource.name[0] # just taking the first of available full names
            self.name=format_None_to_null_string(name_item.family)
            if name_item.given:
                for given in name_item.given:
                    self.name+=", "+given
        else:
            self.name=""

        
        if patient_resource.address is not None:
            self.address=format_address_item(address_item=patient_resource.address[0]) # just taking first of available addresses  
        else:
            self.address=""
        
        self.dob=format_None_to_null_string(patient_resource.birthDate)
        self.gender=format_None_to_null_string(patient_resource.gender)