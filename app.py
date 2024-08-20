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
