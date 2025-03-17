from .parse_value import parse_value_entity
class PathReportComponents():
    __slots__=[
        "message_header",
        "diagnostic_report",
        "patient",
        "service_requests",
        "specimens",
        "primary_observations"
        ]


    def __init__(
        self,
        resources_by_fullUrl=None, 
        resources_by_type=None
        ):
        """ 
        start from MessageHeader and follow references through DiagnosticReport
        to Patient, ServiceRequests, Specimens, and Observations (only those directly referenced in DiagnosticReport)
        """
        self.message_header=resources_by_type["MessageHeader"][0] # assume there is one and only one
        self.diagnostic_report=resources_by_fullUrl[self.message_header.focus[0].reference.strip()] # assume this reference exists
        self.patient=resources_by_fullUrl[self.diagnostic_report.subject.reference] # assume this reference exists

        self.service_requests=       [resources_by_fullUrl[x.reference] for x in self.diagnostic_report.basedOn]
        self.specimens=              [resources_by_fullUrl[x.reference] for x in self.diagnostic_report.specimen]
        self.primary_observations=   [resources_by_fullUrl[x.reference] for x in self.diagnostic_report.result]