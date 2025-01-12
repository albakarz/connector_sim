import logging
import socket

# Configure logging for Communicator1 (TCP)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Communicator1 - TCP] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def tcp_client():
    """Sends a TCP message to the connector and receives a response."""
    logging.info("Attempting to connect to connector via TCP on port 5000...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect(("connector", 5000))
        
        message = "Hello from Communicator 1 (TCP)"
        logging.info(f"Sending message: {message}")
        tcp_socket.send(message.encode())

        response = tcp_socket.recv(1024).decode()
        logging.info(f"Received response: {response}")

if __name__ == "__main__":
    tcp_client()