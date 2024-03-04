FROM python:3.9.5-slim-buster
# Install docker client
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update && apt-get install -y docker-ce-cli
# Mount Docker socket
VOLUME /var/run/docker.sock

WORKDIR /app
COPY requirements.txt /app/requirements.txt 
RUN pip install -r requirements.txt
COPY ./server.py /app/server.py
COPY ./service-account.json /app/service-account.json
USER root
CMD ["python", "server.py"]
