# Chatterbox Docker
This repository contains the Docker setup for the Chatter Connector and underlying services, collecively known as the Chatterbox. To run this application, a node ID and key are required from Chatter. Please contact Chatter to obtain these credentials.

## Compatibility
This Docker setup has been tested on the following platforms:
- Linux - ARMv7 (32-bit) architecture (Raspberry Pi)
- Windows - x86_64 (64-bit) architecture (Docker Desktop / WSL2)
- MacOS - x86_64 (64-bit) architecture (Docker Desktop)

## Prerequisites
- Docker
- Docker Compose

### Install Docker
To install Docker, run the following commands:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Install Docker Compose
To install Docker Compose, run the following commands:

**For x86_64 (64-bit) architecture:**
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**For ARMv7 architecture (Raspberry Pi):**
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-armv7" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
[Docker Compose Releases](https://github.com/docker/compose/releases)

## Setup
### Clone the Repository
Clone this repository your local machine. First navigate to your desired directory (home directory is recommended `cd ~`) and run the following commands:
```bash
git clone https://github.com/Chatter-Software-Development/chatterbox-docker.git
cd chatterbox-docker
```

### Environment Variables
Create a .env file in the root directory of the repository and add the necessary environment variables:

```bash
cp .env.example .env
nano .env
```

Update the .env file with the appropriate `BOX_ID` and `KEY` values provided to you by Chatter.

```
BOX_ID=your_box_id
KEY=your_key
```

### Running the Docker Containers
To build and run the Docker containers, execute the following command:

```bash
docker-compose up --build -d
```

Make sure it's running:
    
```bash
docker ps
```

## Deploying as a Service (Linux Only)
To ensure that the Docker containers start automatically on boot, follow these steps to create a systemd service:

### Automatic Service Creation

To automatically create the systemd service, navigate into the repository directory and run the following commands:

```bash
chmod +x create-service.sh
sudo ./create-service.sh
```

This script will create a systemd service file to run the Docker containers as a service on boot. After running successfully, you should restart and verify the service is running.

Available arguments:
- `-d` - Specify the directory where the repository is located (default: current directory)
- `-u` - Specify the username to run the service as (default: current user)
- `-g` - Specify the group to run the service as (default: docker)

### Manual Service Creation
Create a new systemd service file:

```bash
sudo nano /etc/systemd/system/chatterbox.service
```
Add the following content to the service file (make sure to update `WorkingDirectory`, `User`, and `Group` with the appropriate values):

```ini
[Unit]
Description=Chatterbox Application Service
Requires=docker.service
After=docker.service

[Service]
WorkingDirectory=/home/pi/chatterbox-docker
ExecStart=/usr/local/bin/docker-compose up --build -d
ExecStop=/usr/local/bin/docker-compose down
Restart=always
User=pi
Group=docker

[Install]
WantedBy=multi-user.target
```

### Enable and Start the Service
Enable the service to start on boot and start it immediately:

```bash
sudo systemctl enable chatterbox.service
sudo systemctl start chatterbox.service
```

### Verify the Service
Check the status of the service to ensure it is running correctly:

```bash
sudo systemctl status chatterbox.service
```

Make sure the Docker containers are running:

```bash
docker ps
```

### Reboot the System
Reboot the SBC to verify that the Docker containers start automatically on boot:

```bash
sudo reboot
```

With these steps, your Docker containers for the Chatterbox application should be set to run automatically on boot.

## License
The license for this repository is available in the LICENSE file.