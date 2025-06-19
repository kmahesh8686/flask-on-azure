from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Track how many responses we've assigned
assigned_count = 0

@app.route('/warmup', methods=['GET', 'POST'])
def warmup():
    """This endpoint is used to make a dummy connection to reduce latency."""
    print("[Warmup] Connection established")
    return jsonify({'status': 'ok', 'message': 'Connection warmed up'})

@app.route('/assign', methods=['POST'])
def assign():
    global assigned_count

    data = request.get_json()
    options = data.get('options', [])

    if not isinstance(options, list) or len(options) == 0:
        return jsonify({'status': 'error', 'message': 'Invalid or missing "options" list'}), 400

    if assigned_count < len(options):
        assigned = options[assigned_count]
        print(f"[Assigned {assigned_count + 1}] {assigned}")
    else:
        assigned = options[0]  # fallback is the first item of the latest request
        print(f"[Fallback used] {assigned}")

    assigned_count += 1

    return jsonify({'status': 'ok', 'assigned': assigned})

# Optional block for running locally (not used by Azure)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
