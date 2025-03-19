#!/usr/bin/python

import sys

sys.path.append("../viewer")

from process_path_lab_test_report.process_fhir_bundle_report_to_text import process_fhir_bundle_report_to_text

report_fhir_bundle_filename=sys.argv[1]
text_report_strings=process_fhir_bundle_report_to_text(
    filename=report_fhir_bundle_filename)
print("\n".join(text_report_strings))

