# IP Geolocation Display App for Azar Chat

This project is a simple application designed for use with the Azar chat app. It captures IP addresses during WebRTC connections and displays geolocation data in a GUI window. The application consists of a JavaScript snippet that runs in the browser and a Python Flask server that handles geolocation requests and displays the results using Tkinter.

## Features

- Captures public IP addresses from WebRTC connections in the Azar chat app.
- Sends the captured IP addresses to a local Python server.
- Performs geolocation lookups using the `ipinfo.io` API.
- Displays geolocation data in a Tkinter GUI window.

## Requirements

- **Browser:** Google Chrome (Firefox has CORS restrictions that may prevent the script from working correctly).
- **Python:** Version 3.x with the following packages:
  - `flask`
  - `requests`
  - `tkinter`
  - `flask-cors`

## Installation

### 1. Clone the repository

``git clone https://github.com/adhdlinux/Azar-Live-IP-Geolocator.git``
``cd ip-geolocation-display``

### 2. Install Python dependencies

Ensure you have Python 3 installed. You can install the required Python packages using `pip`:

``pip3 install flask requests flask-cors``

### 3. Set up the JavaScript in your Browser

1. Open Google Chrome.
2. Open the Developer Console (F12 or right-click > Inspect).
3. Navigate to the **Console** tab.
4. Copy and paste the JavaScript code from the `js-script.js` file into the console.

### 4. Running the Python Server

#### On Linux or macOS

1. Open a terminal.
2. Navigate to the project directory.
3. Run the Python server:

   ``python3 server.py``

#### On Windows

1. Open Command Prompt or PowerShell.
2. Navigate to the project directory.
3. Run the Python server:

   ``python3 server.py``

## Usage

1. After running the Python server, paste the JavaScript code into Chrome's Developer Console while using the Azar chat app.
2. As WebRTC connections are established in Azar, the captured IP addresses will be sent to the Python server.
3. The Tkinter GUI window will display the geolocation data for each captured IP address.

## Known Issues

- The script only works on Google Chrome due to CORS restrictions in Firefox.
- The Python server must be running on the same machine as the browser.
- This tool is specifically designed for the Azar chat app and may not work with other applications.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
