from flask import Flask, jsonify
import json

app = Flask(__name__)
DATA_FILE = '/data/data.json'

@app.route('/data', methods=['GET'])
def get_data():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
