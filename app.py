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
import uuid

def run_shell_script(script, vcf, snp_list, uid):
    stdout = subprocess.run([script, vcf, snp_list, uid],capture_output=True).stdout.decode('utf-8')
    return stdout

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/parsevcf', methods=['GET', 'POST'])
def parsevcf():
    if request.method == 'POST':
        file = request.data
        uid = str(uuid.uuid4())
        filename = uid + '.vcf'
        # if user does not select file, browser also
        # submit an empty part without filename
        if file:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f: 
                f.write(file)
            filename = secure_filename(filename)
            run_shell_script('./grabProjectSNPs.sh',os.path.join(app.config['UPLOAD_FOLDER'], filename), uid + "SNPs.txt", uid)
            results = pd.read_csv(uid + "results.txt", sep='\t', header=None)
            os.remove(uid + "myProjectSNPs.out")
            os.remove(uid + "projectGenotype.out")
            os.remove(uid + "refProjectGenotype.out")
            os.remove(uid + "onlyRefProjectSNPs.txt")
            return Response(results.to_json(orient ="records"), mimetype='application/json')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
