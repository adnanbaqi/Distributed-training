import json  # Import the JSON module to handle JSON data
import pyotp  # Import the pyotp module to handle TOTP (Time-Based One-Time Password)
import requests  # Import the requests module to make HTTP requests
from utils.cryptography import encrypt, generate_fernet_key_from_totp_secret  # Import specific cryptographic functions from a utility module

# Fixed the base URL string for the API endpoint
base_url = "http://127.0.0.1:5000/v1"

# Properly formatted headers dictionary for authorization and content type
headers = {
    "Authorization": 'Bearer [LONG AUTH TOKEN]',  # Authorization header with bearer token  ### MAKE SURE TO ADD AUTH TOKEN HERE [LONG AUTH TOKEN]
    "Content-Type": 'application/json'  # Set content type as JSON
}

# Perform a POST request to initiate a session and get TOTP data
session_response = requests.post(base_url + "/totp/session", json={"machine_id": "abcd123"}, headers=headers)
session_data = session_response.json()  # Parse the JSON response into a Python dictionary
print('Session Data: \n', session_data)  # Print the session data

# Generate a TOTP code using the secret received from the session response
totp_code = pyotp.TOTP(session_data["totp_secret"]).now()

# Encrypt the payload using TOTP-based generated Fernet key
encrypted_payload = encrypt(
    json.dumps({
        "totp_code": totp_code,  # Include the TOTP code in the payload
        "data": "test_data"  # Include some additional data (e.g., 'test_data')
    }).encode("utf-8"),  # Encode the JSON string to bytes
    generate_fernet_key_from_totp_secret(session_data["totp_secret"])  # Generate a Fernet key from the TOTP secret
)

print('Encrypted Payload: \n', encrypted_payload)  # Print the encrypted data

# Update headers for sending encrypted data; change content type to plain text and add session token
headers.update({
    "Content-Type": "text/plain",  # Update content type to plain text for encrypted data
    "Session-Token": session_data['token']  # Include the session token in headers
})

# Send the encrypted payload to the encryption endpoint
encryption_response = requests.post(base_url + "/encryption", data=encrypted_payload.decode(), headers=headers)
print("Encryption was sucessful, data recorded on immudb ::", encryption_response.status_code)  # Print the status code of the response to check if it was successful
