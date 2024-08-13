from flask import Flask, request, jsonify
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
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
        self.text_area = ScrolledText(root, wrap=tk.WORD, height=20, width=60)
        self.text_area.pack(padx=10, pady=10)
        self.text_area.insert(tk.END, "Received IP Addresses:\n")

    def append_text(self, text):
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.yview(tk.END)  # Auto-scroll to the bottom

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
        app_gui.append_text(f"Geolocation data for IP {ip}: {geo_data}")
        
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
