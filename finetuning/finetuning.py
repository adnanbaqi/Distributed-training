import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import AutoTokenizer
import requests
import logging
import datetime
import os
import json
from dotenv import load_dotenv
from petals import AutoDistributedModelForCausalLM
import subprocess
import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='LOGS/training.log',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# Load environment variables
load_dotenv()

def print_current_time():
    current_time = datetime.datetime.now()
    print(f"Current system time: {current_time}")


def check_and_sync_time():
    print("Checking initial system time:")
    print_current_time()

    try:
        subprocess.run(['sudo', 'ntpdate', 'pool.ntp.org'], check=False)
        print("Time synchronized successfully.")
    except FileNotFoundError:
        print("ntpdate is not installed. Installing now...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ntpdate'])
        print("Attempting to synchronize time after installation:")
        subprocess.run(['sudo', 'ntpdate', 'pool.ntp.org'])
    except subprocess.CalledProcessError:
        print("Failed to synchronize time. Check your network connection or server availability.")

    print("Final system time after attempting synchronization:")
    print_current_time()


# Authentication header retrieval
check_and_sync_time()

def get_auth_header():
    token = os.getenv("GLOBAL_AUTH_TOKEN")
    return {"Authorization": f"Bearer {token}"}

class FastAPIDataset(Dataset):
    def __init__(self, session_id, tokenizer, max_length=512):
        super().__init__()
        self.session_id = session_id
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.data, self.meta_data = self.fetch_data(session_id)

    def fetch_data(self, session_id):
        fetch_url = f"http://localhost:8000/api/v1/load/{session_id}"
        headers = get_auth_header()
        response = requests.get(fetch_url, headers=headers)
        if response.status_code == 200:
            data = response.json()['data']
            texts = [data['text']]
            meta_data = {
                "language": data['language'],
                "num_tokens": data['num_tokens'],
                "provider_id": data['provider_id'],
                "validator_id": data['validator_id']
            }
            return texts, meta_data
        else:
            raise Exception(f"Failed to fetch data for session ID {session_id}: HTTP status code {response.status_code}")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data[idx]
        encoding = self.tokenizer(text, return_tensors='pt', max_length=self.max_length, truncation=True, padding="max_length")
        input_ids = encoding['input_ids'].squeeze()  # Remove the batch dimension
        attention_mask = encoding['attention_mask'].squeeze()
        return input_ids, attention_mask

# Initialize model and tokenizer
model_name = "deepseek-ai/deepseek-coder-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
session_id = "84625a1658ba405683a83a597e4bf7b5"
dataset = FastAPIDataset(session_id, tokenizer)
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

# Device setup for training
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = AutoDistributedModelForCausalLM.from_pretrained(model_name, initial_peers=['/ip4/45.79.153.218/tcp/31337/p2p/QmXfANcrDYnt5LTXKwtBP5nsTMLQdgxJHbK3L1hZdFN8km']).to(device)

# Model parameter setup
for name, param in model.named_parameters():
    logging.info(f"{name} requires grad: {param.requires_grad}")
    if not param.requires_grad:
        param.requires_grad = True

optimizer = AdamW(model.parameters(), lr=5e-5)
num_epochs = 1

# Training loop
start_time = datetime.datetime.now()
logging.info(f"Fine-tuning started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
for epoch in range(num_epochs):
    model.train()
    for input_ids, attention_mask in dataloader:
        input_ids, attention_mask = input_ids.to(device), attention_mask.to(device)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        logging.info(f"Epoch {epoch+1}, Loss: {loss.item()}")

end_time = datetime.datetime.now()
logging.info(f"Fine-tuning ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

training_data = {
    "message": "Fine-tuning the model was successfully completed",
    "session_id": session_id,
    "loss": "{:.9f}".format(loss.item()),  # Format loss to three decimal places
    "end_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "language": dataset.meta_data['language'],
    "num_tokens": dataset.meta_data['num_tokens'],
    "provider_id": dataset.meta_data['provider_id'],
    "validator_id": dataset.meta_data['validator_id']
}

# Write data to a text file in the specified format
with open('training_data.txt', 'w') as f:
    for key, value in training_data.items():
        f.write(f"{key}: {value}\n")

# Save the model
model.save_pretrained("./models")
