from flask import Flask, request, jsonify
import threading
import tkinter as tk
import requests
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

# Setup error logging
logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s"
)

load_dotenv()
app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("IPINFO_API_KEY", "65a1e552358bd2")
API_URL = f"https://ipinfo.io/{{}}/json?token={API_KEY}"
THREATPIPES_API_KEY = os.getenv("THREATPIPES_API_KEY", "your_threatpipes_api_key")
THREATPIPES_API_URL = "https://api.threatpipes.com/v1/ip/{}"

class IPDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Geolocator")
        self.labels = {}
        fields = [
            ("IP", "ip"), ("Hostname", "hostname"), ("City", "city"), ("Region", "region"),
            ("Country", "country"), ("Location", "loc"), ("Org", "org"), ("Postal", "postal"),
            ("Timezone", "timezone"), ("Risk Score", "risk_score"), ("Blacklisted", "blacklisted"),
            ("Abuse Types", "abuse_types"), ("Last Reported", "last_reported")
        ]
        for name, key in fields:
            label = tk.Label(root, text=f"{name}: N/A", anchor="w")
            label.pack(fill=tk.X, padx=5, pady=2)
            self.labels[key] = label

    def update_labels(self, data):
        for key in ["ip", "hostname", "city", "region", "country", "loc", "org", "postal", "timezone"]:
            self.labels[key].config(text=f"{key.capitalize()}: {data.get(key, 'N/A')}")
        threat_data = data.get("threat_data", {})
        self.labels["risk_score"].config(text=f"Risk Score: {threat_data.get('risk_score', 'N/A')}")
        self.labels["blacklisted"].config(text=f"Blacklisted: {threat_data.get('blacklisted', 'N/A')}")
        abuse_types = ", ".join(threat_data.get("abuse_types", [])) if threat_data.get("abuse_types") else "None"
        self.labels["abuse_types"].config(text=f"Abuse Types: {abuse_types}")
        self.labels["last_reported"].config(text=f"Last Reported: {threat_data.get('last_reported', 'N/A')}")
        print("Updated GUI with IP data:", data)

def get_geolocation(ip):
    try:
        response = requests.get(API_URL.format(ip), timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error("Geolocation error", exc_info=True)
        print(f"Geolocation error: {e}")
        return {}

def get_threat_intelligence(ip):
    try:
        headers = {"Authorization": f"Bearer {THREATPIPES_API_KEY}"}
        response = requests.get(THREATPIPES_API_URL.format(ip), headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "risk_score": data.get("risk_score", "N/A"),
            "blacklisted": "Yes" if data.get("blacklisted", False) else "No",
            "abuse_types": data.get("abuse_types", []),
            "last_reported": data.get("last_reported_at", "Never")
        }
    except Exception as e:
        logging.error("Threat intelligence error", exc_info=True)
        print(f"Threat intelligence error: {e}")
        return {"risk_score": "N/A", "blacklisted": "N/A", "abuse_types": [], "last_reported": "N/A"}

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        ip = request.json.get('ip')
        print(f"Received IP: {ip}")
        geo_data = get_geolocation(ip)
        geo_data['ip'] = ip
        geo_data['threat_data'] = get_threat_intelligence(ip)
        app_gui.update_labels(geo_data)
        return jsonify({"status": "success", "data": geo_data})
    except Exception as e:
        logging.error("Error processing request", exc_info=True)
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    root = tk.Tk()
    app_gui = IPDisplayApp(root)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    root.mainloop()
