from fastapi import FastAPI
from websocket import websocket_endpoint

app = FastAPI(
    title="AI Drawing Showdown Backend",
    version="1.0.0"
)



@app.get("/")
def home():
    return {
        "message": "Welcome to AI Drawing Showdown Backend!",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }

app.websocket("/ws")(websocket_endpoint)