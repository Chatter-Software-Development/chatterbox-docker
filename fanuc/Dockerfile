FROM mcr.microsoft.com/dotnet/runtime:3.1

WORKDIR /app

COPY . /app/

RUN chmod +x /app/linux-x86_64/CHATTER-FANUC.dll
RUN chmod +x /app/linux-armv7/CHATTER-FANUC.dll
# RUN chmod +x /app/CHATTER-FANUC.dll
ENV LD_LIBRARY_PATH=/app

WORKDIR /app

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]