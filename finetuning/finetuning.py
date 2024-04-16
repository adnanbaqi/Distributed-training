<<<<<<< HEAD
# from Petals_pipeline.timemanager.NTPserver import sync_time
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import AutoTokenizer
import requests
from petals import AutoDistributedModelForCausalLM
import datetime
import os
import subprocess

def check_and_sync_time():
    try:
        # Try running ntpdate to check if it is installed
        subprocess.run(['sudo', 'ntpdate', 'pool.ntp.org'], check=True)
    except FileNotFoundError:
        # If not installed, install it (you may need to use a different package manager depending on the OS)
        print("ntpdate is not installed. Installing now...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ntpdate'])
        # After installation, synchronize time
        subprocess.run(['sudo', 'ntpdate', 'pool.ntp.org'])

check_and_sync_time()

class FastAPIDataset(Dataset):
    def __init__(self, session_id, tokenizer, max_length=512):
        super().__init__()
        self.session_id = session_id
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.data, self.meta_data = self.fetch_data(session_id)

    def fetch_data(self, session_id):
        fetch_url = f"http://localhost:8000/api/v1/load/{session_id}" 
        response = requests.get(fetch_url)
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

model_name = "deepseek-ai/deepseek-coder-7b-instruct"  # The Model has a better EVAL score>>
tokenizer = AutoTokenizer.from_pretrained(model_name)

INITIAL_PEERS = ['/ip4/45.79.153.218/tcp/31337/p2p/QmXfANcrDYnt5LTXKwtBP5nsTMLQdgxJHbK3L1hZdFN8km']

session_id = "5f6125a7a5b5431490acc88e256518be"  ############################### Provide the specific session ID
dataset = FastAPIDataset(session_id, tokenizer)
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = AutoDistributedModelForCausalLM.from_pretrained(model_name, initial_peers=INITIAL_PEERS).to(device)

for name, param in model.named_parameters():
    print(f"{name} requires grad: {param.requires_grad}")
    if not param.requires_grad:
        param.requires_grad = True

optimizer = AdamW(model.parameters(), lr=5e-5)
num_epochs = 1

# Print the datetime at which fine-tuning began
start_time = datetime.datetime.now()
print(f"Fine-tuning started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

for epoch in range(num_epochs):
    model.train()  # Ensure the model is in training mode
    for input_ids, attention_mask in dataloader:
        input_ids, attention_mask = input_ids.to(device), attention_mask.to(device)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss

        optimizer.zero_grad()  # Clear previous gradients
        loss.backward()  # Compute gradient of the loss with respect to model parameters
        optimizer.step()  # Update model parameters

        print(f"Epoch {epoch+1}, Loss: {loss.item()}")

end_time = datetime.datetime.now()
print(f"Fine-tuning ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Print the additional metadata
print(f"Session ID: {session_id}")
print(f"Language: {dataset.meta_data['language']}")
print(f"Number of Tokens: {dataset.meta_data['num_tokens']}")
print(f"Provider ID: {dataset.meta_data['provider_id']}")
print(f"Validator ID: {dataset.meta_data['validator_id']}")
print("Fine-Tuning The Model Was Sucessfully Completed...!")

# Save the model
model.save_pretrained("./models")
=======
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import AutoTokenizer
import requests
from petals import AutoDistributedModelForCausalLM  # Assuming this is a valid import based on your script

FETCH_URL = "http://localhost:8000/api/v1/load"

class FastAPIDataset(Dataset):
    def __init__(self, fetch_url, tokenizer, max_length=512):
        super().__init__()
        self.tokenizer = tokenizer
        self.data = self.fetch_data(fetch_url)
        self.max_length = max_length

    def fetch_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['data']
            texts = [item['value'] for item in data]
            return texts
        else:
            raise Exception(f"Failed to fetch data: HTTP status code {response.status_code}")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data[idx]
        encoding = self.tokenizer(text, return_tensors='pt', max_length=self.max_length, truncation=True, padding="max_length")
        input_ids = encoding['input_ids'].squeeze()  # Remove the batch dimension
        attention_mask = encoding['attention_mask'].squeeze()
        return input_ids, attention_mask

model_name = "deepseek-ai/deepseek-coder-7b-instruct-v1.5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
INITIAL_PEERS = ['/ip4/45.79.153.218/tcp/31337/p2p/QmXfANcrDYnt5LTXKwtBP5nsTMLQdgxJHbK3L1hZdFN8km']
model = AutoDistributedModelForCausalLM.from_pretrained(model_name, initial_peers=INITIAL_PEERS).cuda()

# Ensure all model parameters require gradients
for param in model.parameters():
    param.requires_grad = True

dataset = FastAPIDataset(FETCH_URL, tokenizer)
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

optimizer = AdamW(model.parameters(), lr=5e-5)

num_epochs = 1
for epoch in range(num_epochs):
    model.train()  # Ensure the model is in training mode
    for input_ids, attention_mask in dataloader:
        input_ids, attention_mask = input_ids.to(device), attention_mask.to(device)

        # Clear previous gradients
        optimizer.zero_grad()

        # Forward pass: Compute predicted y by passing x to the model
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss

        # Backward pass: Compute gradient of the loss with respect to model parameters
        loss.backward()

        # Calling the step function on an Optimizer makes an update to its parameters
        optimizer.step()

        print(f"Epoch {epoch+1}, Loss: {loss.item()}")

# Save the model
model.save_pretrained("./models")
>>>>>>> 7aa2d69bbe4397e655a20c8a90b2d3c45df56c0e
