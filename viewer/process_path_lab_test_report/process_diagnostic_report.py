from .utils import format_address_item, format_None_to_null_string

class DiagnosticReportData():
    __slots__=[
        "report_id",
        "issued_date",
        "provider_name",
        "provider_address",
        "notes",
        "conclusion",
        ]

    def __init__(self, diagnostic_report=None, resources_by_fullUrl=None):
        if diagnostic_report.identifier is not None:
            self.report_id=diagnostic_report.identifier[0].value # just take first identifier
        else:
            self.report_id=""
        self.issued_date=format_None_to_null_string(diagnostic_report.issued)
        self.provider_name=resources_by_fullUrl[diagnostic_report.performer[0].reference].name       # assumes only one performer, that reference exists,
        self.provider_address=format_address_item(resources_by_fullUrl[diagnostic_report.performer[0].reference].address[0]) # and that it is an Organization with one address
        self.conclusion=format_None_to_null_string(diagnostic_report.conclusion)
        self.notes=[]
        if diagnostic_report.extension is not None:
            for extension in diagnostic_report.extension:
                if extension.url=="http://hl7.org/fhir/5.0/StructureDefinition/extension-DiagnosticReport.note":
                    if extension.valueAnnotation is not None:
                        self.notes.append(extension.valueAnnotation.text) # only use valueAnnotation