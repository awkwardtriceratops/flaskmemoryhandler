from flask import Flask, request, jsonify
from clickhouse_connect import get_client
from datetime import datetime
from flask_cors import CORS 
import os

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Initialize ClickHouse client using environment variables
client = get_client(
    host=os.getenv('CH_HOST'),
    user=os.getenv('CH_USER'),
    password=os.getenv('CH_PASS'),
    secure=True
)

@app.route('/api/add', methods=['POST'])
def add_entry():
    data = request.get_json()  # parse JSON body :contentReference[oaicite:5]{index=5}
    note = data.get('note')
    mental_score = data.get('mentalScore')

    # Prepare row: [datetime, note, mentalScore]
    row = [
        datetime.utcnow(),  # DateTime column
        note,               # String column
        float(mental_score) # Float32 column
    ]

    # Insert into mainMemory table in default database :contentReference[oaicite:6]{index=6}
    client.insert(
        table='mainMemory',
        data=[row],
        column_names=['datetime', 'note', 'mentalScore']
    )

    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    app.run(port=5000, debug=True)
