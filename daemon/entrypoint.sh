#!/bin/sh

mkdir -p /root/.config/Chatter

echo "{
  \"boxID\": \"${BOX_ID}\",
  \"key\": \"${KEY}\",
  \"version\": \"0.0\"
}" > /root/.config/Chatter/config.json

python /app/chatterdaemon.py