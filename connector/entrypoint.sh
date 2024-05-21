#!/bin/sh

# Exit, not yet implemented
echo "ChatterConnector is not yet implemented, please run the Chatter Desktop Connector"
exit 1

mkdir -p /root/.config/Chatter

echo "{
  \"boxID\": \"${BOX_ID}\",
  \"key\": \"${KEY}\",
  \"version\": \"0.0\"
}" > /root/.config/Chatter/config.json

/app/ChatterConnector --nogui