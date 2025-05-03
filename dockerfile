FROM python:3.12.10-slim-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && \
apt-get install -y curl sudo && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

# Cria o usuário batman
RUN useradd -ms /bin/bash batman

# Permite que batman use sudo apenas para update-ca-certificates e curl, sem senha
RUN echo "batman ALL=(ALL) NOPASSWD: /usr/sbin/update-ca-certificates, /usr/bin/curl" > /etc/sudoers.d/batman && \
    chmod 0440 /etc/sudoers.d/batman

COPY app.py .

USER batman

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]