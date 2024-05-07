

```markdown
Distributed Training

# Introduction

This repository houses the code for an innovative data processing and analysis pipeline designed to efficiently handle and process large volumes of data.
Leveraging cutting-edge technologies and algorithms, the Petals Pipeline aims to provide a robust and scalable solution for data scientists and developers alike.

## Features
- Data Tokenization and Analysis: Automated processing of incoming data, including tokenization, language detection, and token count.
- Secure Data Storage: Utilizing immudb for secure, key-value storage of processed data.
- Enhanced Security in V2: Future updates will include TOTP-based encryption and decryption for enhanced data security.
- Compatibility and Library Support: Including support for the Petals library and a workaround for UVLoop on Windows platforms named `WinLoop`.

## Setup

**Set Up Environment Variables**:
- Rename `env.example` to `.env`
- Edit the `.env` file to include your specific configuration values.

### Installation

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

### Development Mode
To start the server in development mode, use the following command:

`uvicorn main:app --reload`

*Additionally you can add custom port definitions too*  
Use --port {YOUR_PORT_NO.}

This starts the Uvicorn server with automatic reloading at `http://127.0.0.1:8000`. 
The `--reload` flag ensures the server updates instantly upon code changes. 
It also allows access to real-time interactive API documentation:- Swagger UI: `http://127.0.0.1:8000/docs`

### Prerequisites

- Docker
- Python 3.8 or later
- WSL

```

# REST API Documentation

### 1. POST `/api/v1/store`

#### Brief Description
This endpoint stores the data provided by the user..!

#### JSON Parameters

| FIELD          | TYPE   | DESCRIPTION                                                                           |
|----------------|--------|---------------------------------------------------------------------------------------|
| Provider_ID    | string | Must be `\w-` and must be between 1 and 64 length.                                    |
| Validator_ID   | UUID   | Uniqque Identifer for Validators                                                      |
| Token_Lenght   | int    | Provides a tokenized token lenght                                                     |
| Language       | str    | Determines the coding language for that specific Code snippet                         |
| Wallet_id      | UUID   | Unique Identifier Id for the Wallet                                                   |

#### Success Response Body

The successful response returns the following fields in JSON format:

| FIELD       | TYPE   | DESCRIPTION                                                                     |
|-------------|--------|---------------------------------------------------------------------------------|
| Session_ID  | string | The token is alphanumeric (a-zA-Z0-9) and 32 characters in length.              |
| totp_secret | string | Base32 encoded, 32-character alphanumeric string, uppercase letters and digits. |


## Authentication

**All API requests require the use of a Bearer token in the header.**




4.1 To run the container, open WSL and run the Client_runner

```bash
sudo docker run -p 31330:31330 --ipc host --gpus all --volume petals-cache:/cache --rm \learningathome/petals:main \python -m petals.cli.run_server --port 31330 deepseek-ai/deepseek-coder-7b-instruct --public_name {YOUR_NAME} --initial_peers /ip4/45.79.153.218/tcp/31337/p2p/QmXfANcrDYnt5LTXKwtBP5nsTMLQdgxJHbK3L1hZdFN8km 
```

## Common Errors

Errors across all endpoints are returned in a standard format, as shown in the table below:

| Error Code | Description                                |
|------------|--------------------------------------------|
| 405        | Method Not Allowed                         |
| 422        | Unprocessable Entity - Invalid parameters. |
| 500        | Internal Server Error.                     |


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please open an issue on the GitHub repository.
``` adnanbaqi.work@gmail.com ```

