from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Security configuration (in production, use environment variables)
API_SECRET_TOKEN = "aegisx-secure-auth-2026"

# In-memory advanced telemetry store
active_devices = {}
activity_logs = []


def log_event(message):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    activity_logs.insert(0, f"[{timestamp}] {message}")
    if len(activity_logs) > 50:
        activity_logs.pop()


@app.route("/")
def tracker_page():
    return render_template("tracker.html")


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@app.route("/api/update_location", methods=["POST"])
def update_location():
    # Verify Token Authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_SECRET_TOKEN}":
        return (
            jsonify({"status": "error", "message": "Unauthorized telemetry key"}),
            401,
        )

    data = request.get_json()
    device_id = data.get("device_id")
    lat = data.get("latitude")
    lon = data.get("longitude")
    accuracy = data.get("accuracy")
    speed = data.get("speed", 0.0)

    if not device_id or lat is None or lon is None:
        return jsonify({"status": "error", "message": "Invalid telemetry payload"}), 400

    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    # Initialize device record if new
    if device_id not in active_devices:
        active_devices[device_id] = {
            "path": [],  # Stores historical coordinates for breadcrumb trails
            "history_timestamps": [],
        }

    # Append current coordinate to path history (max 50 points per device)
    current_path = active_devices[device_id]["path"]
    new_point = [lat, lon]
    if not current_path or current_path[-1] != new_point:
        current_path.append(new_point)
        if len(current_path) > 50:
            current_path.pop(0)

    active_devices[device_id].update(
        {
            "latitude": lat,
            "longitude": lon,
            "accuracy": round(accuracy, 1) if accuracy else None,
            "speed": round(speed * 3.6, 1) if speed else 0.0,  # m/s to km/h
            "last_seen": datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
            "ip_address": client_ip,
        }
    )

    log_event(
        f"Telemetry packet received from '{device_id}' | Pos: ({lat:.4f}, {lon:.4f})"
    )
    return jsonify({"status": "success"})


@app.route("/api/locations", methods=["GET"])
def get_locations():
    return jsonify({"devices": active_devices, "logs": activity_logs[:20]})


@app.route("/api/stop_sharing", methods=["POST"])
def stop_sharing():
    data = request.get_json()
    device_id = data.get("device_id")
    if device_id in active_devices:
        del active_devices[device_id]
        log_event(f"Session terminated by device '{device_id}'")
    return jsonify({"status": "stopped"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)