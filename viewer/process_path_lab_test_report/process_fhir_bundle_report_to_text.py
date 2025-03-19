#!/usr/bin/python

import sys

from .parse_bundle_message import parse_bundle_message
from .process_report_observations import process_report_observations
from .process_path_report_bundle import PathReportComponents
from .process_specimen import SpecimenData
from .process_patient import PatientData
from .process_diagnostic_report import DiagnosticReportData
from .process_service_request import ServiceRequestData
from .utils import format_None_to_null_string

def process_fhir_bundle_report_to_text(
    filename=None, 
    flask_FileStorage=None,
    path_report_components=None, # this is so tests can maniulate the components and pass them in
    resources_by_fullUrl=None,   # ditto
    ):
    
    # This routine can be called from a Flask app or a plain script
    # It accepts either 
    #     a filename 
    #     a flask FileStorage object 
    # These are passed on to parse_bundle_message which handle the distinction
    # (depending on which one is not None)
    # OR it accepts the pre parsed and processed path_report_components and resources_by_full_Url for running tests
    
    if path_report_components is None: # this is usually the case, when a filename or flask FileStorage object is passed in 
        resources_by_fullUrl, resources_by_type, failure_info=parse_bundle_message(
            filename=filename,
            flask_FileStorage=flask_FileStorage,
            )
        
        if failure_info is not None:
            return failure_info
        
        # diagnostic_report, patient, service_requests, specimens, primary_observations=follow_references(
        path_report_components=PathReportComponents(
            resources_by_fullUrl=resources_by_fullUrl, 
            resources_by_type=resources_by_type,
            )

    text_report_strings=[f"(Processed message starts)"] # This is used by test scripts
    text_report_strings.append(f"") 


    # text_report_strings.append(f"dr: {diagnostic_report.id}")
    # text_report_strings.append(f"p: {patient.id}")
    # text_report_strings.append(f"sr: {[x.id for x in service_requests]}")
    # text_report_strings.append(f"sp: {[x.id for x in specimens]}")
    # text_report_strings.append(f"po: {[x.id for x in primary_observations]}")
    
    text_report_strings.append(f"PATIENT")
    patient_data=PatientData(patient_resource=path_report_components.patient)
    text_report_strings.append(f"NHS Number: {patient_data.nhs_number}")
    text_report_strings.append(f"Name:       {patient_data.name}")
    text_report_strings.append(f"Address:    {patient_data.address}")
    text_report_strings.append(f"DOB:        {patient_data.dob}")
    text_report_strings.append(f"Gender:     {patient_data.gender}")

    for i_service_request,service_request in enumerate(path_report_components.service_requests):
        text_report_strings.append("")
        text_report_strings.append(f"SERVICE_REQUEST ({i_service_request+1})")      
        service_request_data=ServiceRequestData(service_request=service_request, resources_by_fullUrl=resources_by_fullUrl)
        text_report_strings.append(f"Request Id:        {service_request_data.request_id}")
        text_report_strings.append(f"Requisition Id:    {service_request_data.requisition_id}")
        text_report_strings.append(f"Requested test:    {service_request_data.requested_test}")
        text_report_strings.append(f"Requester:         {service_request_data.requester}")
        text_report_strings.append(f"Request date:      {service_request_data.request_date}")
        text_report_strings.append(f"Clinical details:  {service_request_data.clinical_details}")
        text_report_strings.append(f"Comments:")
        for note in service_request_data.notes:
            text_report_strings.append(f"{note}")

    for i_specimen, specimen in enumerate(path_report_components.specimens):
        text_report_strings.append("")
        text_report_strings.append(f"SPECIMEN ({i_specimen+1})") 
        specimen_data=SpecimenData(specimen=specimen)
        text_report_strings.append(f"Requester Specimen Id:   {specimen_data.requester_specimen_id}")
        text_report_strings.append(f"Laboratory Accession Id: {specimen_data.laboratory_accession_id}")
        text_report_strings.append(f"Specimen Type:           {specimen_data.specimen_type}")
        text_report_strings.append(f"Collected Date:          {specimen_data.collected_date}")
        text_report_strings.append(f"Received Date:           {specimen_data.received_date}")
        text_report_strings.append(f"Comments:")
        for note in specimen_data.notes:
            text_report_strings.append(f"{note}")

    diagnostic_report_data=DiagnosticReportData(
        diagnostic_report=path_report_components.diagnostic_report, 
        resources_by_fullUrl=resources_by_fullUrl,
        )
    text_report_strings.append("")
    text_report_strings.append(f"REPORT")
    text_report_strings.append(f"Report Id:        {diagnostic_report_data.report_id}")
    text_report_strings.append(f"Issued Date:      {diagnostic_report_data.issued_date}")
    text_report_strings.append(f"Provider Name:    {diagnostic_report_data.provider_name}")
    text_report_strings.append(f"Provider Address: {diagnostic_report_data.provider_address}")
    text_report_strings.append(f"Comments:")
    for note in diagnostic_report_data.notes:
        text_report_strings.append(f"{note}")
    
    output_strings=process_report_observations(
        primary_observations=path_report_components.primary_observations,
        resources_by_fullUrl=resources_by_fullUrl,
        )
    text_report_strings.append("")
    text_report_strings.append(f"RESULTS")
    for output_string in output_strings:
        text_report_strings.append(output_string)

    conclusion=format_None_to_null_string(diagnostic_report_data.conclusion)
    text_report_strings.append("")
    text_report_strings.append(f"Diagnostic Report Conclusion:" )
    text_report_strings.append(f"{conclusion}" )

    text_report_strings.append(f"") 
    text_report_strings.append(f"(End of processed message)") # This is used by test scripts to check that seemed to complete

    return text_report_strings

if __name__=="__main__":
    report_fhir_bundle_filename=sys.argv[1]
    text_report_strings=process_fhir_bundle_report_to_text(
        filename=report_fhir_bundle_filename)
    print("\n".join(text_report_strings))
    
