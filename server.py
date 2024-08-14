from flask import Flask, request, jsonify
import threading
import tkinter as tk
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# API Key for IP geolocation service (replace with your own API key)
API_KEY = "65a1e552358bd2"
API_URL = "https://ipinfo.io/{}/json?token=" + API_KEY

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

    def update_labels(self, data):
        # Update each label with the latest data
        self.ip_label.config(text=f"IP: {data.get('ip', 'N/A')}")
        self.hostname_label.config(text=f"Hostname: {data.get('hostname', 'N/A')}")
        self.city_label.config(text=f"City: {data.get('city', 'N/A')}")
        self.region_label.config(text=f"Region: {data.get('region', 'N/A')}")
        self.country_label.config(text=f"Country: {data.get('country', 'N/A')}")
        self.loc_label.config(text=f"Location: {data.get('loc', 'N/A')}")
        self.org_label.config(text=f"Organization: {data.get('org', 'N/A')}")
        self.postal_label.config(text=f"Postal Code: {data.get('postal', 'N/A')}")
        self.timezone_label.config(text=f"Timezone: {data.get('timezone', 'N/A')}")

        # Log the data in the terminal
        print("\nGeolocation Data:")
        for key, value in data.items():
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

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        ip = data.get('ip', 'No IP provided')
        print(f"Received IP: {ip}")
        
        # Perform geolocation lookup
        geo_data = get_geolocation(ip)
        geo_data['ip'] = ip  # Include the IP in the response data

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
