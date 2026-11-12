# SentialStream (AegisX Sentinel)

**SentialStream** is an advanced, consent-based real-time telemetry and location-tracking operations platform built for cybersecurity reconnaissance, asset tracking, and live field unit monitoring. It combines a secure Python Flask backend with an interactive Leaflet.js mapping interface and a Tailwind CSS dark-mode command center.

---

## Key Features

* **Consent-Based Geolocation Beacon:** Uses the HTML5 Geolocation API (`navigator.geolocation.watchPosition`) to transmit coordinates only with explicit browser permission.
* **Token-Based API Security:** Endpoints are protected with Bearer token authentication to prevent unauthorized payload injection.
* **Movement Breadcrumb Trails:** Automatically plots historical path polylines on the live map to visualize a device's movement over time.
* **Real-Time Command Center:** Features live telemetry cards, speed/accuracy meters, and encrypted audit logging.
* **Multi-Device Support:** Tracks multiple independent field units simultaneously on a single centralized map.

---

## Tech Stack

* **Backend:** Python 3, Flask (REST API, in-memory telemetry state manager)
* **Frontend UI:** Tailwind CSS (Modern dark-mode tactical interface)
* **Mapping:** Leaflet.js & OpenStreetMap tiles (Client-side rendering, no proprietary API keys required)

---

## Project Structure

```text
SentialStream/
├── requirements.txt
├── app.py
└── templates/
    ├── tracker.html     # Client beacon transmitter page
    └── dashboard.html   # Operations command center map dashboard
