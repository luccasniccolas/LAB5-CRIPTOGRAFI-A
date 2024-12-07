FROM ubuntu:16.10

# Actualizar repositorios para versiones EOL y configurar apt
RUN sed -i 's/archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y openssh-client && apt-get clean

CMD ["/bin/bash"]
