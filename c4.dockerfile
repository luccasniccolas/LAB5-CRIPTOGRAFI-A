FROM ubuntu:22.10

# Actualizar repositorios para versiones EOL y configurar apt
RUN sed -i 's/archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y openssh-client openssh-server && apt-get clean

# Configuración inicial para el servidor SSH
RUN mkdir -p /var/run/sshd && \
    echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config && \
    useradd -m -s /bin/bash prueba && echo "prueba:prueba" | chpasswd

# Exponer el puerto 22 para SSH
EXPOSE 22

# Comando para iniciar el servidor SSH
CMD ["/usr/sbin/sshd", "-D"]
