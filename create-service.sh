#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Must run as root."
  exit 1
fi

if ! command -v docker &> /dev/null; then
  echo "docker is not installed. Please install docker."
  exit 1
fi

if ! command -v docker-compose &> /dev/null; then
  echo "docker-compose is not installed. Please install docker-compose."
  exit 1
fi

# Default values
WORKING_DIRECTORY=$(pwd)
CURRENT_USER=${SUDO_USER}
DOCKER_GROUP="docker"
SERVICE_NAME="chatterbox.service"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}"
DOCKER_COMPOSE_PATH="/usr/local/bin/docker-compose"

# Parse arguments
while getopts "d:u:g:" opt; do
  case ${opt} in
    d )
      WORKING_DIRECTORY=$OPTARG
      ;;
    u )
      CURRENT_USER=$OPTARG
      ;;
    g )
      DOCKER_GROUP=$OPTARG
      ;;
    \? )
      echo "Usage: cmd [-d] [-u] [-g]"
      exit 1
      ;;
  esac
done

if [ ! -f "${WORKING_DIRECTORY}/docker-compose.yml" ]; then
  echo "Error: docker-compose.yml not found in the working directory. Are you sure you are in the correct directory?"
  exit 1
fi

if [[ $(basename "$WORKING_DIRECTORY") != "chatterbox-docker" ]]; then
  echo "Error: working directory is not called \"chatterbox-docker\". Are you sure you are in the correct directory?"
  exit 1
fi

# Check if the specified group exists
if ! getent group "${DOCKER_GROUP}" >/dev/null; then
  echo "Group '${DOCKER_GROUP}' does not exist. Please create the group and add the user to it and retry, or create the service manually."
  exit 1
fi

# Check if the specified user belongs to the specified group
if ! id -nG "${CURRENT_USER}" | grep -qw "${DOCKER_GROUP}"; then
  echo "User '${CURRENT_USER}' does not belong to the '${DOCKER_GROUP}' group. Please add the user to the group and retry, or create the service manually."
  exit 1
fi

# Create the service file
echo "Creating service file at ${SERVICE_PATH}..."
echo "[Unit]
Description=Chatterbox Docker Service
Requires=docker.service
After=docker.service

[Service]
WorkingDirectory=${WORKING_DIRECTORY}
ExecStart=${DOCKER_COMPOSE_PATH} up --build -d
ExecStop=${DOCKER_COMPOSE_PATH} down
Restart=always
User=${CURRENT_USER}
Group=${DOCKER_GROUP}

[Install]
WantedBy=multi-user.target" | sudo tee "${SERVICE_PATH}"

# Reload systemd, enable and start the service
echo "Reloading systemd and starting the service..."
sudo systemctl daemon-reload
sudo systemctl enable "${SERVICE_NAME}"
sudo systemctl start "${SERVICE_NAME}"

echo "Service ${SERVICE_NAME} created and started successfully."
echo "To check the status of docker containers, run \`docker ps\`"
echo "For further support, please visit https://github.com/Chatter-Software-Development"