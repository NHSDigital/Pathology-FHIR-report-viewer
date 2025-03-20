#!/usr/bin/python
"""
This script checks how gracefully the report making routine handles missing elements in a pathology report message Bundle

The script parses a well populated message Bundle and selectively sets a range of elements to None

Each time round the main loop a different element is set to None (and the whole process below repeated)

After modification of a specific resource element the bundle is reconstructed into a temp file

The temp file is then processed by the report making script and the output is monitored for
(i) uncaught exceptions
(ii) whether something odd enough has happened (judged by the standard last line of the output not being present)

The output report is shown along with a summary line of the apparent outcome

The summary line contains "TEXT_SUMMARY:" at the start so output can be filtered for simply those lines if desired
"""

import os, sys, tempfile, copy, traceback

from fhir.resources.R4B.bundle import Bundle, BundleEntry # not sure why but R4B seems needed or get error parsing bundle

sys.path.append("../viewer")

from process_path_lab_test_report.process_fhir_bundle_report_to_text import process_fhir_bundle_report_to_text
from process_path_lab_test_report.parse_bundle_message import parse_bundle_message
from process_path_lab_test_report.process_path_report_bundle import PathReportComponents

def create_temp_file_from_bundle(
    resources_by_type=None,
    resources_by_fullUrl=None,
    ):

    ###################
    # recreate bundle #
    ###################

    bundle=Bundle(type="message")
    bundle.entry=[]
    bundle.entry.append(BundleEntry(resource=resources_by_type["MessageHeader"][0]))

    for fullUrl, resource in resources_by_fullUrl.items():
        bundle.entry.append(BundleEntry(resource=resource, fullUrl=fullUrl))

    #####################
    # save as temp file #
    #####################
    
    fp=tempfile.NamedTemporaryFile(mode='w', prefix="path_report_viewer_testing_", suffix='.json',  delete=False)
    fp.write(bundle.json())
    fp.close()
    return fp

def delete_temp_file(fp=None):
    os.remove(fp.name)  # trying using delete_on_close=True in NamedTemporaryFile gave
                        #     TypeError: NamedTemporaryFile() got an unexpected keyword argument 'delete_on_close'
                        # for reason do not understand, so manually deleting instead


report_fhir_bundle_filename=sys.argv[1] # this should be an example bundle that processes well and has a high degree of populated elements

###############
# "main loop" #
###############

for resource_name, element in [
    ["patient", "identifier"],
    ["patient", "name"],
    # [patient, "name[0]"],    # this is illegal in the bundle and only want to test things here that pass bundle parsing
    ["patient", "name[0].family"],
    ["patient", "name[0].given"],
    ["patient", "address"],
    ["patient", "address[0].line"],
    ["patient", "address[0].city"],
    ["patient", "address[0].district"],
    ["patient", "address[0].postalCode"],
    ["patient", "birthDate"],
    ["patient", "gender"],
    ["service_request", "identifier"],
    ["service_request", "requisition"],
    ["service_request", "requester"],
    ["service_request", "authoredOn"],
    ["service_request", "code"],
    ["service_request", "code.coding"],
    # [service_request, "code.coding[0]"], # this gives an illegal bundle as above
    ["service_request", "code.coding[0].code"],
    ["service_request", "code.coding[0].display"],
    ["service_request", "reasonCode"],
    ["service_request", "note"],
    ["specimen",        "identifier"],
    ["specimen",        "accessionIdentifier"],
    ["specimen",        "type"],
    ["specimen",        "type.coding"],
    ["specimen",        "type.coding[0].display"],
    ["specimen",        "collection"],
    ["specimen",        "collection.collectedDateTime"],
    ["diagnostic_report", "identifier"],
    ["diagnostic_report", "issued"],
    #this code cannot follow references, or extensions so cannot test DiagnosticReportData.notes or .provider_name or .provide_address
    ]:

    print("##########################################################################")
    print("##########################################################################")
    
    element_spec=f"{resource_name}.{element}"

    print(f"TESTING: {element_spec}")
        
    ###############################################################################
    # Process the bundle file from scratch every time round loop so that do not   #
    # have to undo the modifications made below                                   #
    ###############################################################################    
    
    resources_by_fullUrl, resources_by_type, failure_info=parse_bundle_message(
        filename=report_fhir_bundle_filename,
        )
    path_report_components=PathReportComponents(
        resources_by_fullUrl=resources_by_fullUrl, 
        resources_by_type=resources_by_type,
        )
    service_request=path_report_components.service_requests[0]  # just test effect in first service request
    specimen=path_report_components.specimens[0]                # just test effect in first specimen
    patient=path_report_components.patient                      
    diagnostic_report=path_report_components.diagnostic_report
    
    ############################
    # apply the modification   #
    ############################
    
    exec(f"{resource_name}.{element}=None")

    #########################################################
    # recreate bundle as temp file and run processing on it #
    #########################################################

    fp=create_temp_file_from_bundle(
        resources_by_type=resources_by_type,
        resources_by_fullUrl=resources_by_fullUrl,
        )

    failed=False
    text_report_strings=[]
    try:
        text_report_strings=process_fhir_bundle_report_to_text(filename=fp.name)
    except Exception as exception:
        print("")
        print("".join(traceback.format_exception(exception)))
        failed=True

    delete_temp_file(fp)
    
    ###############
    # make output #
    ###############

    print("\n".join(text_report_strings))

    if failed:
        message="ERROR: Code raised an uncaught exception. See details above"
    elif text_report_strings[-1]!="(End of processed message)":
        message="ERROR: Output ended unexpectedly. See details above"
    else:
        message="OK:    Processing apparently finished OK"
    
    print(f"TEST_SUMMARY: {element_spec:40} : {message}")
    