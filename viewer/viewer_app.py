
import traceback

from flask import Flask, render_template, request

from process_path_lab_test_report.process_fhir_bundle_report_to_text import process_fhir_bundle_report_to_text

app = Flask(__name__)

######################
######################
## app health check ##
######################
######################

@app.route("/healthy")
def healthy():
    return "<p>The app is running</p>"

###############
###############
## main page ##
###############
###############

@app.route('/', methods=['GET','POST'])
def path_validator():
   
    data_to_show="No data yet"
    filename="No file loaded yet"
    if 'uploaded_file' in request.files:
        try:
            text_report_strings=process_fhir_bundle_report_to_text(
                flask_FileStorage=request.files['uploaded_file']
                )
        except Exception as exception:
            text_report_strings=["An unhandled error occurred:"]
            text_report_strings.append("".join(traceback.format_exception(exception)))
        
        data_to_show="<pre>"+"<br>".join(text_report_strings)
        # data_to_show="report will be here"
        filename=request.files['uploaded_file'].filename
        
    return render_template('viewer.html',
                            data_to_show=data_to_show,
                            filename=filename,
                            )

app.run(debug=True, host='0.0.0.0', port=5001)