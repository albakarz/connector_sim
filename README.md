# Simulation Project (Local Version)

This project demonstrates how to **bridge different communication protocols** (TCP, UDP, and HTTP) using a single **connector** service. Each protocol is represented by a “communicator” microservice, and all services run as separate Docker containers on **one** local machine.

---

## 1. Architecture Overview

```

┌───────────────────┐      ┌───────────────────┐      ┌─────────────────────┐
│ Communicator 1    │      │ Communicator 2    │      │ Communicator 3      │
│ (TCP)             │      │ (UDP)             │      │ (HTTP)              │
│   sends TCP       │      │   sends UDP       │      │   sends POST        │
└─────────┬─────────┘      └─────────┬─────────┘      └─────────┬───────────┘
          │                          │                          │
          │ TCP:5000                 │ UDP:5001                 │ HTTP:5002
          │                          │                          │
          ▼                          ▼                          ▼
        ┌─────────────────────────────────────────────────────────┐
        │                           Connector                     │
        │          - Listens for TCP on port 5000                 │
        │          - Listens for UDP on port 5001                 │
        │          - Hosts a Flask app for HTTP on port 5002      │
        └─────────────────────────────────────────────────────────┘

```

1. **Connector**:  
   - A Python service that listens on **TCP:5000**, **UDP:5001**, and **HTTP:5002**.  
   - Receives messages from each communicator and sends back a response.  
2. **Communicator 1 (TCP)**:  
   - Simulates a device sending messages over TCP.  
3. **Communicator 2 (UDP)**:  
   - Simulates a device sending messages over UDP.  
4. **Communicator 3 (HTTP)**:  
   - Uses an HTTP POST request to communicate with the connector’s Flask endpoint.

---

## 2. Project Structure

Below is the expected directory layout:

```

simulation_project/
│
├── connector/
│   ├── Dockerfile
│   └── connector.py
│
├── communicator1/
│   ├── Dockerfile
│   └── communicator1.py
│
├── communicator2/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── communicator2.py
│
├── communicator3/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── communicator3.py
│
├── docker-compose.yml
└── README.md

```

Each communicator has its own Dockerfile and Python script. The `connector` folder contains a Flask app and socket-based servers for TCP/UDP.

---

## 3. Prerequisites

1. **Docker** (latest version)  
   - [Install Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)  
   - [Install Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)  
   - [Install Docker Engine on Linux](https://docs.docker.com/engine/install/)  

2. **Docker Compose**  
   - Usually bundled with Docker Desktop.  
   - On newer Docker versions, `docker-compose` may be replaced by `docker compose` (the plugin). Both commands behave similarly.

Make sure Docker is running before you proceed.

---

## 4. Setup Instructions

### 4.1 Cloning or Downloading

1. Clone this repository (or download and unzip):
   ```bash
   git clone https://github.com/<your-username>/simulation_project.git
   cd simulation_project

	2.	Confirm the folder structure matches what’s shown above.

4.2 Building Docker Images

# From inside the simulation_project/ folder:
docker-compose build

	•	This command will build four images:
	1.	simulation_project-connector
	2.	simulation_project-communicator1
	3.	simulation_project-communicator2
	4.	simulation_project-communicator3

4.3 Starting the Containers

docker-compose up

	•	Connector starts first, listens on ports 5000 (TCP), 5001 (UDP), and 5002 (HTTP).
	•	Communicator1 (TCP) connects to connector:5000.
	•	Communicator2 (UDP) sends to connector:5001.
	•	Communicator3 (HTTP) sends a POST to http://connector:5002/http.

5. Verifying the Setup

As docker-compose up runs, you’ll see logs from each container in your terminal:
	1.	Connector:

[INFO] [Connector] TCP handler started. Listening on port 5000.
[INFO] [Connector] UDP handler started. Listening on port 5001.
[INFO] [Connector] HTTP handler starting. Listening on port 5002.

This means the connector is ready to receive on all three protocols.

	2.	Communicator1 (TCP) might log:

[Communicator1 - TCP] Attempting to connect to connector via TCP on port 5000...
[Communicator1 - TCP] Sending message: Hello from Communicator 1 (TCP)
[Communicator1 - TCP] Received response: [Connector -> TCP] Successfully received your message: Hello from Communicator 1 (TCP)

This shows a successful TCP round trip.

	3.	Communicator2 (UDP) might log:

[Communicator2 - UDP] Sending a UDP message to connector on port 5001...
[Communicator2 - UDP] Sending message: Hello from Communicator 2 (UDP)
[Communicator2 - UDP] Received response: [Connector -> UDP] Got your message: Hello from Communicator 2 (UDP)

Confirmation that UDP messages also flow correctly.

	4.	Communicator3 (HTTP) might log:

[Communicator3 - HTTP] Sending POST to http://connector:5002/http with payload: {'message': 'Hello from Communicator 3 (HTTP)'}
[Communicator3 - HTTP] Received response [200]: {'response': '[Connector -> HTTP] Received your message: ...'}

Indicates the Flask server processed the POST successfully and returned a JSON response.

After they send their messages, communicator1, communicator2, and communicator3 usually exit with code 0, while the connector container keeps running until you stop it.

6. Additional Commands
	•	View logs for a specific container:

docker-compose logs connector

or

docker-compose logs communicator1


	•	Stop and remove containers:

docker-compose down


	•	Rebuild (if you change the code in any communicator or connector):

docker-compose build

7. Troubleshooting
	•	“Port already in use”
	•	Something on your system is using port 5000, 5001, or 5002.
	•	Either stop the service occupying that port or change the port mapping in docker-compose.yml.
	•	No logs from a communicator
	•	Check if it exited prematurely with an error:

docker-compose logs communicator1


	•	Make sure your code references ("connector", 5000) (or 5001, 5002) inside Docker. Docker Compose sets up an internal hostname “connector” for that container.

	•	Permission / Firewall issues
	•	On some systems, you may need to allow Docker’s inbound connections or disable local firewalls for containers to communicate.
