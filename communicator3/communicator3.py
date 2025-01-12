import logging
import requests

# Configure logging for Communicator3 (HTTP)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Communicator3 - HTTP] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def http_client():
    """Sends an HTTP POST to the connector and prints the JSON response."""
    url = "http://connector:5002/http"
    payload = {"message": "Hello from Communicator 3 (HTTP)"}
    
    logging.info(f"Sending POST to {url} with payload: {payload}")
    response = requests.post(url, json=payload)
    
    logging.info(f"Received response [{response.status_code}]: {response.json()}")

if __name__ == "__main__":
    http_client()