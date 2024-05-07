<p align="center">
  <img src="https://github.com/Immutableai/metex-health-monitor/blob/main/static/logo.jpg" width="100">
</p>
<p align="center">
    <h1 align="center">PETALS-ML-INFERENCE</h1>
</p>
<p align="center">
    <em>Empower ML Inference with Petals Efficiency!</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/languages/top/FerrariDG/async-ml-inference?style=flat&color=blueviolet" alt="repo-top-language">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Pydantic-E92063.svg?style=flat&logo=Pydantic&logoColor=white" alt="Pydantic">
	<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=FastAPI&logoColor=white" alt="FastAPI">
</p>



# 📍 Introduction To Distributed Training

This repository houses the code for an innovative data processing and analysis pipeline designed to efficiently handle and process large volumes of data.
Leveraging cutting-edge technologies and algorithms, the Petals Pipeline aims to provide a robust and scalable solution for data scientists and developers alike.

## 🧩 Features
- Data Tokenization and Analysis: Automated processing of incoming data, including tokenization, language detection, and token count.
- Secure Data Storage: Utilizing immudb for secure, key-value storage of processed data.
- Enhanced Security in V2: Future updates will include TOTP-based encryption and decryption for enhanced data security.
- Compatibility and Library Support: Including support for the `Petals` library and a workaround for UVLoop on Windows platforms named `WinLoop`.

---

## 🗂️  Repository Structure

```sh
└── distributed_training/
    ├───Client_request
    ├───controller
    ├───Docker
    │   └───Petals_docker
    ├───finetuning
    ├───ImmuDB_Binaries
    ├───LOGS
    ├───schemas
    ├───session_enc
    ├───template
    ├───time
    └───tools
```

---



## ⚙️ Setup

**Set Up Environment Variables**:
- Rename `env.example` to `.env`
- Edit the `.env` file to include your specific configuration values.

### 🛠 Installation

1. Clone the repository:
```bash
git clone https://github.com/adnanbaqi/Distributed_Training-.git
```

2. Navigate to the project directory:
```bash
cd Distributed-Training
```

3. Install required Python libraries:
```bash
pip install -r requirements.txt
```

### 🧪 Development Mode
To start the server in development mode, use the following command:

`uvicorn main:app --reload`

*Additionally you can add custom port definitions too*  
Use --port {YOUR_PORT_NO.}

This starts the Uvicorn server with automatic reloading at `http://127.0.0.1:8000`. 
The `--reload` flag ensures the server updates instantly upon code changes. 
It also allows access to real-time interactive API documentation:- Swagger UI: `http://127.0.0.1:8000/docs`

### 📦 Prerequisites

- Docker
- Python 3.10
- WSL 2.0

# ⚡️ REST API Documentation

### 1. POST `/api/v1/store`

#### Brief Description
This endpoint stores the data provided by the user..!

#### JSON Parameters

| FIELD          | TYPE   | DESCRIPTION                                                                           |
|----------------|--------|---------------------------------------------------------------------------------------|
| Provider_ID    | str    | Must be `\w-` and must be between 1 and 64 length.                                    |
| Validator_ID   | UUID   | Unique Identifer for Validators                                                       |

| Language       | str    | Determines the coding language for that specific Code snippet                         |
| Wallet_id      | UUID   | Unique Identifier Id for the Wallet                                                   |

#### Success Response Body

The successful response returns the following fields in JSON format:

| FIELD          | TYPE   | DESCRIPTION                                                                     |
|----------------|--------|---------------------------------------------------------------------------------|
| Session_ID     | string | The token is alphanumeric (a-zA-Z0-9) and 32 characters in length.              |
| Token_Lenght   | int    | Provides a tokenized token lenght                                               |

<details>
<summary>Example JSON </summary>

```json
{
 "text": Data,
 "language": Python,
 "num_tokens": 2342,
 "provider_id": immutablelabsai,
 "validator_id": 5dab608d-46f5-43dc-a7c8-586bfcbe4c85,
 "wallet_id": 123e4567-e89b-12d3-a456-426614174000 
}
```
</details>

### 2. GET `/api/v1/load`

#### Brief Description
This Endpoint is used to retrieve the confidential data uploaded by the provider.

#### Headers

| HEADER            | TYPE   | DESCRIPTION                                                    |
|-------------------|--------|----------------------------------------------------------------|
| Global_Auth_Token | string | The token must be alphanumeric.                                |

#### Payload

The request body must contain an encrypted string prepared according to the [Encryption Process](#encryption-process). The structure of the JSON to be encrypted is specified in this section:

| FIELD         | TYPE   | DESCRIPTION                                                                    |
|---------------|--------|--------------------------------------------------------------------------------|
| Session_Id    | string | The token is alphanumeric (a-zA-Z0-9) and 32 characters in length.             |

#### Responses

The response for this endpoint includes:

| Status Code | Description                                                       |
|-------------|-------------------------------------------------------------------|
| 404         | Session id was not found.                                         |
| 505         | Session data retrieved and decoded successfully                   |
| 500         | INTERNAL SERVER ERROR                                             |

### 3. POST `api/v1/finetune`

#### Brief Description
This endpoint is used for passing finetuning requests.
This endpoint is under construction...!

#### Headers

| HEADER        | TYPE   | DESCRIPTION                                                    |
|---------------|--------|----------------------------------------------------------------|
| Auth-Token    | string | The session token must be alphanumeric                         |


#### Payload

| FIELD         | TYPE   | DESCRIPTION                                                         |
|---------------|--------|---------------------------------------------------------------------|
| session_id    | string | The token is alphanumeric (a-zA-Z0-9) and 32 characters in length.  |
| Gpu_id (temp) | string | A unique GPU based id used for request identifications.             |


#### Response

The response for this endpoint includes:

| Status Code | Description                                                       |
|-------------|-------------------------------------------------------------------|
| 200         | Request created sucessfully.                                      |
| 401         | Session token is invalid. Access is denied.                       |
| 403         | GPU id is invalid                                                 |

## 🛡️ Authentication

**All API requests require the use of a Bearer token in the header.**

###To run the container,
#open WSL.
##For Client_runner 

```bash
sudo docker run -p 31330:31330 --ipc host --gpus all --volume petals-cache:/cache --rm \learningathome/petals:main \python -m petals.cli.run_server --port 31330 deepseek-ai/deepseek-coder-7b-instruct --public_name {YOUR_NAME} --initial_peers /ip4/45.79.153.218/tcp/31337/p2p/QmXfANcrDYnt5LTXKwtBP5nsTMLQdgxJHbK3L1hZdFN8km 
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please open an issue on the GitHub repository.
``` adnanbaqi.work@gmail.com ```

