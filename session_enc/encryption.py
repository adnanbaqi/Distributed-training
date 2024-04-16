import requests
import subprocess
import xml.etree.ElementTree as ET
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
import json
from dotenv import load_dotenv
import os

def get_nvidia_gpu_uuid():
    try:
        nvidia_smi_output = subprocess.check_output(["nvidia-smi", "-q", "-x"]).decode('utf-8')
        root = ET.fromstring(nvidia_smi_output)
        gpu_uuid = root.find('.//gpu/uuid')
        return gpu_uuid.text if gpu_uuid is not None else "no_nvidia_gpu_found"
    except Exception as e:
        print(f"Error fetching NVIDIA GPU UUID: {e}")
        return "nvidia_smi_command_failed"

load_dotenv()
global_auth_token = os.getenv('GLOBAL_AUTH_TOKEN')
print("Loaded Global Auth Token:", global_auth_token)

machine_id = get_nvidia_gpu_uuid()
session_url = "http://127.0.0.1:8000/v1/totp/session"
session_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {global_auth_token}",
}
session_data = {
    "machine_id": machine_id, 
    "session_ttl": 3600,
    "totp_digit": 4,
    "totp_interval": 30
}

session_response = requests.post(session_url, json=session_data, headers=session_headers)
if session_response.status_code in [200, 201]:
    print("Session created successfully.")
    session_data = session_response.json()
    session_token = session_data['token']  # This should be the raw token as received
    print("Session Token:", session_token)  # Debug print for the session token

    totp_secret = session_data['totp_secret']
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(totp_secret.encode())
    hashed_secret = digest.finalize()
    fernet_key = urlsafe_b64encode(hashed_secret[:32])
    cipher = Fernet(fernet_key)

    payload = {"data": "Sensitive information to be encrypted"}
    encrypted_payload = cipher.encrypt(json.dumps(payload).encode())

    encryption_url = "http://127.0.0.1:8000/v1/encryption"
    encryption_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {global_auth_token}",
    }
    encryption_data = {
        "session_token": session_token,
        "totp_code": totp_secret,
        "data": encrypted_payload.decode()  
    }

    encryption_response = requests.post(encryption_url, data=encrypted_payload, headers=encryption_headers)
    if encryption_response.status_code == 201:
        print("Data encrypted and stored successfully.")
    else:
        print(f"Encryption failed. Status code: {encryption_response.status_code}")
        print("Response from encryption endpoint:", encryption_response.text)
else:
    print("Failed to create session. Status code:", session_response.status_code)
    print("Response from session endpoint:", session_response.text)
