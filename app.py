from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

# In-memory store
stored_presets = []
default_preset = None
assigned_count = 0
lock = threading.Lock()


@app.route('/set-presets', methods=['POST'])
def set_presets():
    """Receive and store the preset options and default."""
    global stored_presets, assigned_count, default_preset

    data = request.get_json()
    options = data.get('options', [])
    default = data.get('default')

    if not isinstance(options, list) or not options:
        return jsonify({'status': 'error', 'message': 'Invalid or missing options'}), 400
    if not default:
        return jsonify({'status': 'error', 'message': 'Missing default preset'}), 400

    with lock:
        stored_presets = options
        default_preset = default
        assigned_count = 0

    print(f"[Presets Stored] {len(options)} presets, default: {default}")
    return jsonify({'status': 'ok', 'message': f'{len(options)} presets stored with default'})


@app.route('/assign', methods=['GET'])
def assign():
    """Return the next assignment, fallback to default after presets exhausted."""
    global assigned_count

    with lock:
        if not stored_presets or default_preset is None:
            return jsonify({'status': 'error', 'message': 'Presets or default not set'}), 400

        if assigned_count < len(stored_presets):
            assigned = stored_presets[assigned_count]
            print(f"[Assigned {assigned_count + 1}] {assigned}")
            assigned_count += 1
        else:
            assigned = default_preset
            print(f"[Default Returned] {assigned}")

    return jsonify({'status': 'ok', 'assigned': assigned})


@app.route('/warmup', methods=['GET'])
def warmup():
    """Used to establish early connection (cold start prevention)."""
    print("[Warmup] Dummy connection hit")
    return jsonify({'status': 'ok', 'message': 'Connection warmed up'})


# Local testing
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
