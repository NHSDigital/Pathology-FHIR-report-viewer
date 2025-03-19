#!/usr/bin/python

import os, sys, tempfile, copy, traceback

from fhir.resources.R4B.bundle import Bundle, BundleEntry # not sure why but R4B seems needed or get error parsing bundle

sys.path.append("../viewer")

from process_path_lab_test_report.process_fhir_bundle_report_to_text import process_fhir_bundle_report_to_text
from process_path_lab_test_report.parse_bundle_message import parse_bundle_message
from process_path_lab_test_report.process_path_report_bundle import PathReportComponents


def create_temp_file(
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

def set_element_to_None(
    resource=None,
    element=None,
    resources_by_fullUrl=None,
    ):
    test_resource=copy.deepcopy(resource)
    exec(f"test_resource.{element}=None")
    fullUrl=f"urn:uuid:{test_resource.id}"
    resources_by_fullUrl[fullUrl]=test_resource
    element_spec=f"{resource.resource_type}.{element}"
    return element_spec

def restore_element(
    resource=None,
    element=None,
    resources_by_fullUrl=None,
    ):
    fullUrl=f"urn:uuid:{resource.id}"
    resources_by_fullUrl[fullUrl]=resource
    return element_spec

report_fhir_bundle_filename=sys.argv[1]

###########################################
# process bundle into component resources #
# so that can then manipulate them        #
###########################################

resources_by_fullUrl, resources_by_type, failure_info=parse_bundle_message(
    filename=report_fhir_bundle_filename,
    )

path_report_components=PathReportComponents(
    resources_by_fullUrl=resources_by_fullUrl, 
    resources_by_type=resources_by_type,
    )

##################################
# delete service request content #
##################################

service_request=path_report_components.service_requests[0]
specimen=path_report_components.specimens[0]
patient=path_report_components.patient
diagnostic_report=path_report_components.diagnostic_report

for resource, element in [
    [patient, "identifier"],
    [patient, "name"],
    # [patient, "name[0]"],    # this is illegal in the bundle and only want to test things here that pass bundle parsing
    [patient, "name[0].family"],
    [patient, "name[0].given"],
    [patient, "address"],
    [patient, "address[0].line"],
    [patient, "address[0].city"],
    [patient, "address[0].district"],
    [patient, "address[0].postalCode"],
    [patient, "birthDate"],
    [patient, "gender"],
    [service_request, "identifier"],
    [service_request, "requisition"],
    [service_request, "requester"],
    [service_request, "authoredOn"],
    [service_request, "code"],
    [service_request, "code.coding"],
    # [service_request, "code.coding[0]"], # this gives an illegal bundle as above
    [service_request, "code.coding[0].code"],
    [service_request, "code.coding[0].display"],
    [service_request, "reasonCode"],
    [service_request, "note"],
    [specimen,        "identifier"],
    [specimen,        "accessionIdentifier"],
    [specimen,        "type"],
    [specimen,        "type.coding"],
    [specimen,        "type.coding[0].display"],
    [specimen,        "collection"],
    [specimen,        "collection.collectedDateTime"],
    [diagnostic_report, "identifier"],
    [diagnostic_report, "issued"],
    #this code cannot follow references, or extensions so cannot test DiagnosticReportData.notes or .provider_name or .provide_address
    ]:


    element_spec=set_element_to_None(
        resource=resource,
        element=element,
        resources_by_fullUrl=resources_by_fullUrl,
        )

    print(f"{element_spec}")

    ################################
    # recreate bundle as temp file #
    ################################

    fp=create_temp_file(
        resources_by_type=resources_by_type,
        resources_by_fullUrl=resources_by_fullUrl,
        )

    ##################
    # run processing #
    ##################

    failed=False
    text_report_strings=[]
    try:
        text_report_strings=process_fhir_bundle_report_to_text(filename=fp.name)
    except Exception as exception:
        print("")
        print("".join(traceback.format_exception(exception)))
        failed=True
        
    print("\n".join(text_report_strings))

    if failed:
        message="ERROR: Code raised an uncaught exception. See details above"
    elif text_report_strings[-1]!="(End of processed message)":
        message="ERROR: Output ended unexpectedly. See details above"
    else:
        message="OK:    Processing apparently finished OK"
    
    print(f"TEST_SUMMARY: {element_spec:30} : {message}")
    
    delete_temp_file(fp)

    restore_element(  # this is necessary because otherwise the last call to a particular resource leaves that resource in a bad state
        resource=resource,
        element=element,
        resources_by_fullUrl=resources_by_fullUrl,
        )
    





