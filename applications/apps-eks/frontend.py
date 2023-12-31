from flask import Flask, render_template, jsonify, make_response
import os
import sys
import requests
import json

if os.getenv("LATTICEURL") is None or os.getenv("LATTICEURL2") is None:
    print(f'[ERROR] no Lattice URL configured inside Pod')
    sys.exit(1)
else: 
    app = Flask(__name__, template_folder='./templates')
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def home(path): #/backend /lambda
        backend_url = "{}/{}".format(os.getenv("LATTICEURL"), path)
        backend_url_2 = "{}/{}".format(os.getenv("LATTICEURL2"), path)
        if path == "backend":
            print(backend_url) #debug
            try:
                backend_call = requests.get(backend_url).text
                region = json.loads(backend_call)
            except OSError as e:
                return("Something went wrong, check Lattice URL")
            return render_template("index.html", icon = 'static/images/eks.png', message = "Powered by:", aws_reg = region['message'] )
        elif path == "lambda":
            try:
                region = requests.get(backend_url).text
            except OSError as e:
                return("Something went wrong, check Lattice URL")
            return render_template("index.html", icon = 'static/images/lambda.png', message = "Powered by:", aws_reg = region)
        elif path == "vmc":
            try:
                response = requests.get(backend_url_2).text
            except OSError as e:
                return("Something went wrong, check Lattice URL")
            return render_template("index.html", icon = 'static/images/vmware-cloud-aws.jpeg', message = "Powered by:", aws_reg = response)
        else:
            return("Please specify /backend /lambda /vmc path")
        
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=8080)