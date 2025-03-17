from .utils import format_none_to_null_string
class ServiceRequestData():
    __slots__=[
        "request_id",
        "requested_test",
        "requester",
        "request_date",
        "clinical_details",
        "notes",
        "requisition_id"
        ]

    def __init__(self, service_request=None, resources_by_fullUrl=None):
        self.request_id=service_request.identifier[0].value # just take first identifier
        if service_request.requisition is not None:
            self.requisition_id=format_none_to_null_string(service_request.requisition.value)
        else:
            self.requisition_id=""
        requested_coding=service_request.code.coding[0] # just take first coding
        self.requested_test=f"{requested_coding.code}:{requested_coding.display}" 
        
        self.request_date=format_none_to_null_string(service_request.authoredOn)
        
        if service_request.reasonCode is not None:
            self.clinical_details=service_request.reasonCode[0].text # just take first reasonCode 
        else:
            self.clinical_details=""
        
        if service_request.note is not None:
            self.notes=[x.text for x in service_request.note]
        else:
            self.notes=[]

        practitioner=resources_by_fullUrl[service_request.requester.reference] # assume reference exists and is to Practitioner
        name=practitioner.name[0] # just taking the first of available full names
        self.requester=f"{format_none_to_null_string(name.family)}, "
        if name.prefix is not None:
            self.requester+=f"{format_none_to_null_string(name.prefix[0])}" # Just use the first name prefix (if any)
        if name.given:
            for given in name.given:
                self.requester+=" "+given