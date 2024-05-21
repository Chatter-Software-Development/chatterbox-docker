#!/bin/sh

echo "{
  \"boxID\": \"${BOX_ID}\",
  \"key\": \"${KEY}\",
  \"handshakeEndpoint\": \"https://apiv2.chatter.dev/com/legacy/fanuc/handshake\",
  \"endpoint\": \"https://apiv2.chatter.dev/com/legacy/fanuc/transactions\"
}" > /app/appSettings.json

# dotnet /app/chatterfanuc-linux-x86_64.dll

ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
  dotnet /app/linux-x86_64/CHATTER-FANUC.dll
elif [ "$ARCH" = "armv7l" ]; then
  dotnet /app/linux-armv7/CHATTER-FANUC.dll
else
  echo "Unsupported architecture: $ARCH"
  exit 1
fi