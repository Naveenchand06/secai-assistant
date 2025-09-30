from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Vulnerable Demo Application"

@app.route('/fetch')
def fetch_data():
    # Using requests without version pinning - likely to have vulnerabilities
    url = request.args.get('url')
    response = requests.get(url)
    return response.text

if __name__ == '__main__':
    app.run(debug=True)
