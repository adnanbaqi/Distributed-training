import requests
import subprocess
import xml.etree.ElementTree as ET
import json
import logging
from dotenv import load_dotenv
import os
import base64
import hashlib
from cryptography.fernet import Fernet
import pyotp

logging.basicConfig(level=logging.INFO)

def get_nvidia_gpu_uuid():
    try:
        nvidia_smi_output = subprocess.check_output(["nvidia-smi", "-q", "-x"]).decode('utf-8')
        root = ET.fromstring(nvidia_smi_output)
        gpu_uuid = root.find('.//gpu/uuid')
        return gpu_uuid.text if gpu_uuid is not None else "no_nvidia_gpu_found"
    except Exception as e:
        logging.error(f"Error fetching NVIDIA GPU UUID: {e}")
        return "nvidia_smi_command_failed"

# Reading the plain text data from 'training_data.txt'
training_data_file = os.path.join(os.getcwd(), 'finetuning', 'training_data.txt')
with open(training_data_file, 'r') as f:
    training_data = f.read()  # Read the file as plain text

def generate_fernet_key_from_totp_secret(totp_secret: str) -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256(totp_secret.encode()).digest())

def encrypt(data: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(data)

load_dotenv()
global_auth_token = os.getenv('GLOBAL_AUTH_TOKEN')
machine_id = get_nvidia_gpu_uuid()
session_url = "http://127.0.0.1:5000/v1/totp/session"
session_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {global_auth_token}",
}
session_data = {
    "machine_id": machine_id,
    "session_ttl": 3600
}
session_response = requests.post(session_url, json=session_data, headers=session_headers)
if session_response.status_code in [200, 201]:
    logging.info("Session created successfully.")
    session_info = session_response.json()
    session_token = session_info['token']
    totp_secret = session_info['totp_secret']
    totp = pyotp.TOTP(totp_secret)
    totp_code = totp.now()
    fernet_key = generate_fernet_key_from_totp_secret(totp_secret)
    # Include the text data in the JSON structure for encryption
    data_to_encrypt = json.dumps({"totp_code": totp_code, "data": training_data}).encode()
    encrypted_payload = encrypt(data_to_encrypt, fernet_key)
    encryption_url = "http://127.0.0.1:5000/v1/encryption"
    encryption_headers = {
        "Accept": "application/json",
        "Content-Type": "text/plain",
        "Authorization": f"Bearer {global_auth_token}",
        "Session-Token": session_token
    }
    encryption_data = encrypted_payload.decode('utf-8')
    encryption_response = requests.post(encryption_url, data=encryption_data, headers=encryption_headers)
    if encryption_response.status_code == 201:
        logging.info("Data encrypted and stored successfully.")
    else:
        logging.error(f"Encryption failed. Status code: {encryption_response.status_code}")
        logging.error(f"Response from encryption endpoint: {encryption_response.text}")
else:
    logging.error(f"Failed to create session. Status code: {session_response.status_code}")
    logging.error(f"Response from session endpoint: {session_response.text}")
# print(training_data)
