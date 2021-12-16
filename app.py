import subprocess
from flask import Flask
from flask import request
from flask import flash, redirect, url_for, render_template, send_from_directory, Response, jsonify
from flask_cors import CORS
import urllib.request
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import pandas as pd
import numpy as np
import json


def run_shell_script(script, vcf, snp_list):
    stdout = subprocess.run([script, vcf, snp_list],capture_output=True).stdout.decode('utf-8')
    return stdout

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#I assume that the fetch request will be in this type of format
# // Select your input type file and store it in a variable
# const input = document.getElementById('fileinput');

# // This will upload the file after having read it
# const upload = (file) => {
#   fetch('http://www.example.net', { // Your POST endpoint
#     method: 'POST',
#     headers: {
#       // Content-Type may need to be completely **omitted**
#       // or you may need something
#       "Content-Type": "You will perhaps need to define a content-type here"
#     },
#     body: file // This is your file object
#   }).then(
#     response => response.json() // if the response is a JSON object
#   ).then(
#     success => console.log(success) // Handle the success response object
#   ).catch(
#     error => console.log(error) // Handle the error response object
#   );
# };


@app.route('/api/parsevcf', methods=['GET', 'POST'])
def parsevcf():
    if request.method == 'POST':
        file = request.data
        filename = 'user.vcf'
        # if user does not select file, browser also
        # submit an empty part without filename
        if file:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f: 
                f.write(file)
            filename = secure_filename(filename)
            run_shell_script('./grabProjectSNPs.sh',os.path.join(app.config['UPLOAD_FOLDER'], filename), "SNPs.txt")
            results = pd.read_csv("results.txt", sep='\t', header=None)
            print(results)
            os.remove("myProjectSNPs.out")
            os.remove("projectGenotype.out")
            os.remove("refProjectGenotype.out")
            os.remove("onlyRefProjectSNPs.txt")
            return Response(results.to_json(orient ="records"), mimetype='application/json')


#below for testing

# @app.route("/testing",methods=['GET',])
# def testingRun():
#     run_shell_script('./grabProjectSNPs.sh',"/Users/gabriellealtman/Downloads/gaby_VCF.vcf.gz", "SNPs.txt")
#     results = pd.read_csv("results.txt", sep='\t', header=None)
#     print(results)
#     # os.remove("myProjectSNPs.out")
#     # os.remove("projectGenotype.out")
#     # os.remove("refProjectGenotype.out")
#     # os.remove("onlyRefProjectSNPs.txt")
#     return Response(results.to_json(orient ="records"), mimetype='application/json')

app.run(debug=True)
