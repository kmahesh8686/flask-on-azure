from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

# In-memory store
stored_presets = []
assigned_count = 0
lock = threading.Lock()


@app.route('/set-presets', methods=['POST'])
def set_presets():
    """Receive and store the preset options once."""
    global stored_presets, assigned_count

    data = request.get_json()
    options = data.get('options', [])

    if not isinstance(options, list) or not options:
        return jsonify({'status': 'error', 'message': 'Invalid or missing options'}), 400

    with lock:
        stored_presets = options
        assigned_count = 0  # Reset assignment count when new options come in

    print(f"[Presets Stored] {len(options)} items")
    return jsonify({'status': 'ok', 'message': f'{len(options)} presets stored'})


@app.route('/assign', methods=['GET'])
def assign():
    """Return the next assignment without needing the presets in request."""
    global assigned_count

    with lock:
        if not stored_presets:
            return jsonify({'status': 'error', 'message': 'No presets stored yet'}), 400

        if assigned_count < len(stored_presets):
            assigned = stored_presets[assigned_count]
            print(f"[Assigned {assigned_count + 1}] {assigned}")
        else:
            assigned = stored_presets[0]  # fallback
            print(f"[Fallback used] {assigned}")

        assigned_count += 1

    return jsonify({'status': 'ok', 'assigned': assigned})


@app.route('/warmup', methods=['GET'])
def warmup():
    """Used to establish early connection (cold start prevention)."""
    print("[Warmup] Dummy connection hit")
    return jsonify({'status': 'ok', 'message': 'Connection warmed up'})


# Optional for local testing
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
