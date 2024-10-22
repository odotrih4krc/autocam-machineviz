import network
import socket
import time
import machine
import json
import urequests  # Ensure this library is available

# Wi-Fi Configuration
SSID = config.SSID
PASSWORD = config.PASSWORD

# Firebase Configuration (secure the connection)
# Use the credentials from config
FIREBASE_URL = config.FIREBASE_URL
FIREBASE_SECRET = config.FIREBASE_SECRET

# Initialize Camera
def init_camera():
    from esp32_camera import Camera
    Camera.init(0, 0, 640, 480)  # Initialize camera with resolution

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        time.sleep(1)
    
    print('Connected to Wi-Fi:', wlan.ifconfig())

# Capture Image and Send for Recognition
def capture_and_recognize():
    init_camera()
    img = Camera.capture()  # Capture image
    
    # Convert image to base64 for sending
    img_b64 = img.encode('base64')
    
    # Send the image to an external API for recognition
    url = "https://api.example.com/recognize"  # Replace with your API endpoint
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"image": img_b64})
    
    response = urequests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("Recognition Result:", result)
        # Send the result to Firebase
        send_to_firebase(result)
    else:
        print("Error in recognition:", response.status_code)

# Function to send data to Firebase
def send_to_firebase(data):
    url = f"{FIREBASE_URL}/recognition_results.json"
    headers = {'Content-Type': 'application/json'}
    
    # Prepare payload
    payload = json.dumps(data)
    
    # Send data to Firebase
    response = urequests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        print("Data successfully sent to Firebase")
    else:
        print("Error sending data to Firebase:", response.status_code)

# Main Loop
def main():
    connect_wifi()
    while True:
        capture_and_recognize()
        time.sleep(10)  # Adjust the interval as needed

if __name__ == '__main__':
    main()