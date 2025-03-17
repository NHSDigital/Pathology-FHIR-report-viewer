from .utils import format_none_to_null_string
class ServiceRequestData():
    __slots__=[
        "request_id",
        "requested_test",
        "requester",
        "request_date",
        "clinical_details",
        "request_note",
        "requisition_id"
        ]

    def __init__(self, service_request=None):
        self.request_id=service_request.identifier[0].value # just take first identifier
        if service_request.requisition is not None:
            self.requisition_id=format_none_to_null_string(service_request.requisition.value)
        else:
            self.requisition_id=""
        requested_coding=service_request.code.coding[0] # just take first coding
        self.requested_test=f"{requested_coding.code}:{requested_coding.display}" 
        self.requester=service_request.requester.display
        self.request_date=format_none_to_null_string(service_request.authoredOn)
        
        if service_request.reasonCode is not None:
            self.clinical_details=service_request.reasonCode[0].text # just take first reasonCode 
        else:
            self.clinical_details=""
        
        if service_request.note is not None:
            self.request_note=[x.text for x in service_request.note]
        else:
            self.request_note=""