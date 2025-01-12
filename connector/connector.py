import logging
import socket
import threading
from flask import Flask, request, jsonify

# Configure the logging for the connector
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Connector] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = Flask(__name__)

def handle_tcp():
    """TCP handler: listens on port 5000 and sends a response back to the client."""
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("0.0.0.0", 5000))
    tcp_socket.listen(5)
    logging.info("TCP handler started. Listening on port 5000.")

    while True:
        conn, addr = tcp_socket.accept()
        data = conn.recv(1024).decode()
        logging.info(f"[TCP Handler] Received from {addr}: {data}")

        # Respond back to the TCP sender
        response_msg = f"[Connector -> TCP] Successfully received your message: {data}"
        conn.send(response_msg.encode())
        conn.close()

def handle_udp():
    """UDP handler: listens on port 5001 and sends a response back to the client."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 5001))
    logging.info("UDP handler started. Listening on port 5001.")

    while True:
        data, addr = udp_socket.recvfrom(1024)
        msg = data.decode()
        logging.info(f"[UDP Handler] Received from {addr}: {msg}")

        # Respond back to the UDP sender
        response_msg = f"[Connector -> UDP] Got your message: {msg}"
        udp_socket.sendto(response_msg.encode(), addr)

@app.route('/http', methods=['POST'])
def handle_http():
    """HTTP handler: listens on port 5002 for POST requests."""
    data = request.json
    logging.info(f"[HTTP Handler] Received POST data: {data}")

    # Respond back to the HTTP sender
    response_msg = f"[Connector -> HTTP] Received your message: {data}"
    return jsonify({"response": response_msg}), 200

if __name__ == "__main__":
    # Start threads for TCP and UDP handlers
    threading.Thread(target=handle_tcp, daemon=True).start()
    threading.Thread(target=handle_udp, daemon=True).start()

    # Start Flask (HTTP) on port 5002
    logging.info("HTTP handler starting. Listening on port 5002.")
    app.run(host="0.0.0.0", port=5002)