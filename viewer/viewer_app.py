from flask import Flask
# from setchks_app.process_path_lab_test_report.process_fhir_bundle_report_to_text import process_fhir_bundle_report_to_text
from process_path_lab_test_report.process_fhir_bundle_report_to_text import process_fhir_bundle_report_to_text

from flask import render_template, request

app = Flask(__name__)

@app.route("/healthy")
def healthy():
    return "<p>The app is running</p>"

######################################
######################################
## path validator endpoint endpoint ##
######################################
######################################

@app.route('/', methods=['GET','POST'])
def path_validator():
   
    data_to_show="No data yet"
    filename="No file loaded yet"
    if 'uploaded_file' in request.files:
        text_report_strings=process_fhir_bundle_report_to_text(
            flask_FileStorage=request.files['uploaded_file']
            )
        data_to_show="<pre>"+"<br>".join(text_report_strings)
        # data_to_show="report will be here"
        filename=request.files['uploaded_file'].filename
        
        
    return render_template('viewer.html',
                            data_to_show=data_to_show,
                            filename=filename,
                            )


app.run(debug=True, host='0.0.0.0', port=5001)