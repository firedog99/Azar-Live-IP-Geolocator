from flask import Flask, request, jsonify
import threading
import tkinter as tk
import requests
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS

# API Key for IP geolocation service
API_KEY = os.getenv("IPINFO_API_KEY", "65a1e552358bd2")  # Fallback to provided key
API_URL = "https://ipinfo.io/{}/json?token=" + API_KEY

# ThreatPipes API configuration
THREATPIPES_API_KEY = os.getenv("THREATPIPES_API_KEY", "your_threatpipes_api_key")  # Replace with actual key
THREATPIPES_API_URL = "https://api.threatpipes.com/v1/ip/{}"

# Create a Tkinter GUI to display IP data
class IPDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Address Display")
        
        # Create labels for displaying geolocation data
        self.ip_label = tk.Label(root, text="IP: ", anchor="w")
        self.ip_label.pack(fill=tk.X, padx=10, pady=2)
        self.hostname_label = tk.Label(root, text="Hostname: ", anchor="w")
        self.hostname_label.pack(fill=tk.X, padx=10, pady=2)
        self.city_label = tk.Label(root, text="City: ", anchor="w")
        self.city_label.pack(fill=tk.X, padx=10, pady=2)
        self.region_label = tk.Label(root, text="Region: ", anchor="w")
        self.region_label.pack(fill=tk.X, padx=10, pady=2)
        self.country_label = tk.Label(root, text="Country: ", anchor="w")
        self.country_label.pack(fill=tk.X, padx=10, pady=2)
        self.loc_label = tk.Label(root, text="Location: ", anchor="w")
        self.loc_label.pack(fill=tk.X, padx=10, pady=2)
        self.org_label = tk.Label(root, text="Organization: ", anchor="w")
        self.org_label.pack(fill=tk.X, padx=10, pady=2)
        self.postal_label = tk.Label(root, text="Postal Code: ", anchor="w")
        self.postal_label.pack(fill=tk.X, padx=10, pady=2)
        self.timezone_label = tk.Label(root, text="Timezone: ", anchor="w")
        self.timezone_label.pack(fill=tk.X, padx=10, pady=2)
        
        # Add labels for ThreatPipes data
        self.threat_header = tk.Label(root, text="--- Threat Intelligence ---", font=("Arial", 10, "bold"), anchor="w")
        self.threat_header.pack(fill=tk.X, padx=10, pady=5)
        
        self.risk_score_label = tk.Label(root, text="Risk Score: ", anchor="w")
        self.risk_score_label.pack(fill=tk.X, padx=10, pady=2)
        
        self.blacklisted_label = tk.Label(root, text="Blacklisted: ", anchor="w")
        self.blacklisted_label.pack(fill=tk.X, padx=10, pady=2)
        
        self.abuse_types_label = tk.Label(root, text="Abuse Types: ", anchor="w")
        self.abuse_types_label.pack(fill=tk.X, padx=10, pady=2)
        
        self.last_reported_label = tk.Label(root, text="Last Reported: ", anchor="w")
        self.last_reported_label.pack(fill=tk.X, padx=10, pady=2)

    def update_labels(self, data):
        # Update geolocation labels
        self.ip_label.config(text=f"IP: {data.get('ip', 'N/A')}")
        self.hostname_label.config(text=f"Hostname: {data.get('hostname', 'N/A')}")
        self.city_label.config(text=f"City: {data.get('city', 'N/A')}")
        self.region_label.config(text=f"Region: {data.get('region', 'N/A')}")
        self.country_label.config(text=f"Country: {data.get('country', 'N/A')}")
        self.loc_label.config(text=f"Location: {data.get('loc', 'N/A')}")
        self.org_label.config(text=f"Organization: {data.get('org', 'N/A')}")
        self.postal_label.config(text=f"Postal Code: {data.get('postal', 'N/A')}")
        self.timezone_label.config(text=f"Timezone: {data.get('timezone', 'N/A')}")
        
        # Update threat intelligence labels
        threat_data = data.get('threat_data', {})
        self.risk_score_label.config(text=f"Risk Score: {threat_data.get('risk_score', 'N/A')}")
        self.blacklisted_label.config(text=f"Blacklisted: {threat_data.get('blacklisted', 'N/A')}")
        abuse_types = threat_data.get('abuse_types', [])
        abuse_text = ", ".join(abuse_types) if abuse_types else "None detected"
        self.abuse_types_label.config(text=f"Abuse Types: {abuse_text}")
        self.last_reported_label.config(text=f"Last Reported: {threat_data.get('last_reported', 'N/A')}")
        
        # Log the data in the terminal
        print("\nGeolocation Data:")
        for key, value in data.items():
            if key != 'threat_data':
                print(f"{key.capitalize()}: {value}")
        
        if threat_data:
            print("\nThreat Intelligence Data:")
            for key, value in threat_data.items():
                print(f"{key.capitalize()}: {value}")

def get_geolocation(ip):
    try:
        response = requests.get(API_URL.format(ip))
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching geolocation data: {e}")
        return {"error": str(e)}

def get_threat_intelligence(ip):
    try:
        headers = {
            "Authorization": f"Bearer {THREATPIPES_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.get(THREATPIPES_API_URL.format(ip), headers=headers)
        response.raise_for_status()
        data = response.json()
        return {
            "risk_score": data.get("risk_score", 0),
            "blacklisted": "Yes" if data.get("blacklisted", False) else "No",
            "abuse_types": data.get("abuse_types", []),
            "last_reported": data.get("last_reported_at", "Never")
        }
    except requests.RequestException as e:
        print(f"Error fetching threat intelligence data: {e}")
        return {}

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        ip = data.get('ip', 'No IP provided')
        print(f"Received IP: {ip}")
        
        # Perform geolocation lookup
        geo_data = get_geolocation(ip)
        geo_data['ip'] = ip  # Include the IP in the response data
        
        # Perform threat intelligence lookup
        threat_data = get_threat_intelligence(ip)
        geo_data['threat_data'] = threat_data
        
        # Display in Tkinter GUI
        app_gui.update_labels(geo_data)
        
        return jsonify({"status": "success", "data": geo_data})
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    root = tk.Tk()
    app_gui = IPDisplayApp(root)
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start Tkinter main loop
    root.mainloop()
