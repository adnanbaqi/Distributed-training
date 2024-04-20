import logging
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from controller.store_data import router as store_router
from controller.load_data import router as load_router  # Importing from the controller directory
# from controller.train_data import router as train_router

# Setup logging
logging.basicConfig(level=logging.INFO, filename='LOGS/endpoint.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Logging that CORS middleware has been added
logging.info("CORS middleware configured.")

# Include routerss
app.include_router(store_router)
app.include_router(load_router)
# app.include_router(train_router)

@app.get("/", response_class=HTMLResponse)
async def get_home():
    logging.info("Home page accessed.")
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Message</title>
    <style>
        body {
            background-color: black;
            color: white;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
</head>
<body>
    <h1>Good To Go Chief...!</h1>
</body>
</html>
'''

logging.info("FastAPI application has been configured.")
