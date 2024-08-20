# safe-content
prevent unsafe content and to do that follow the step bellow
Setting Up the Environment

    Create a Virtual Environment (optional but recommended)

    bash

python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`

Install Required Packages

bash

pip install requests flask

Create a Flask Application

Create a file named app.py:

python

from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# Replace these values with your actual API credentials
API_USER = '1953127141'
API_SECRET = 'NB8LuEjM78HBQbM8f5QWyL8Pt8BvoddV'
WORKFLOW = 'wfl_gQtWU6fQCo0yPMHRdL09j'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    file = request.files['image']
    params = {
        'workflow': WORKFLOW,
        'api_user': API_USER,
        'api_secret': API_SECRET
    }
    files = {'media': file.read()}
    response = requests.post('https://api.sightengine.com/1.0/check-workflow.json', files=files, data=params)
    output = response.json()
    
    if output['status'] == 'failure':
        return jsonify({'error': output['error']})
    
    result = {
        'action': output['summary']['action'],
        'reject_prob': output['summary']['reject_prob'],
        'reject_reason': output['summary']['reject_reason']
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

Create the HTML Frontend

Create a folder named templates, and inside that folder, create a file named index.html:

html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Adult Content Checker</title>
    </head>
    <body>
        <h1>Adult Content Checker</h1>
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="file" id="image" name="image" accept="image/*" required>
            <button type="submit">Check Image</button>
        </form>
        <div id="result"></div>
        <script>
            document.getElementById('uploadForm').addEventListener('submit', function(event) {
                event.preventDefault();
                var formData = new FormData(this);
                fetch('/check', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    var resultDiv = document.getElementById('result');
                    if (data.error) {
                        resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                    } else {
                        resultDiv.innerHTML = `
                            <p>Action: ${data.action}</p>
                            <p>Reject Probability: ${data.reject_prob}</p>
                            <p>Reject Reasons: ${data.reject_reason.join(', ')}</p>
                        `;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        </script>
    </body>
    </html>

Running the Application

    Run the Flask App

    bash

python app.py

Open Your Web Browser

Go to http://127.0.0.1:5000 to see the HTML form. You can upload an image and check if it gets flagged by the Sightengine API.
