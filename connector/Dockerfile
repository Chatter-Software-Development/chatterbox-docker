FROM debian:latest

WORKDIR /app

COPY . /app/

RUN chmod +x /app/ChatterConnector
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]