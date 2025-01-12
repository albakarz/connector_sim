import logging
import socket

# Configure logging for Communicator2 (UDP)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Communicator2 - UDP] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def udp_client():
    """Sends a UDP message to the connector and receives a response."""
    logging.info("Sending a UDP message to connector on port 5001...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        message = "Hello from Communicator 2 (UDP)"
        logging.info(f"Sending message: {message}")
        udp_socket.sendto(message.encode(), ("connector", 5001))

        response, addr = udp_socket.recvfrom(1024)
        logging.info(f"Received response: {response.decode()} from {addr}")

if __name__ == "__main__":
    udp_client()