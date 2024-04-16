import subprocess
import xml.etree.ElementTree as ET
import random
import string
import requests

def generate_session_id(length=20):
    """Generate a random alphanumeric session ID."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_nvidia_gpu_uuid():
    """Fetch the first NVIDIA GPU's UUID using nvidia-smi."""
    try:
        nvidia_smi_output = subprocess.check_output(["nvidia-smi", "-q", "-x"]).decode('utf-8')
        # Parse the XML output
        root = ET.fromstring(nvidia_smi_output)
        # Find the first GPU's UUID
        gpu_uuid = root.find('.//gpu/uuid')
        if gpu_uuid is not None:
            return gpu_uuid.text
        else:
            return "no_nvidia_gpu_found"
    except Exception as e:
        print(f"Error fetching NVIDIA GPU UUID: {e}")
        return "nvidia_smi_command_failed"

# Assuming your FastAPI app is running locally on port 8000
API_URL = "http://127.0.0.1:8000/api/v1/finetune/"

# Generate session ID and fetch GPU ID
session_id = generate_session_id()
gpu_id = get_nvidia_gpu_uuid()
print("SESSION_ID :",session_id)
print("GPU_ID : ",gpu_id)

# Check if GPU ID was successfully fetched
if gpu_id in ["no_nvidia_gpu_found", "nvidia_smi_command_failed"]:
    print(f"Error fetching GPU ID: {gpu_id}")
else:
    # Sample data for the finetune request
    data = {
        "session_id": session_id,
        "gpu_id": gpu_id
    }

    # Make a POST request to the finetune endpoint
    response = requests.post(API_URL, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        print("Response data:", response.json())
    else:
        print("Request failed.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
