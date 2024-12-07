from scapy.all import rdpcap, wrpcap, Raw, IP, TCP

# Archivos de entrada y salida
pcap_original = 'cliente3.pcapng'
pcap_mod = 'mod.pcapng'

# Dirección IP del cliente
ip_cliente = '172.17.0.4'

# Leer los paquetes del archivo PCAP original
paquetes = rdpcap(pcap_original)

# Longitud deseada para el paquete
tamaño_deseado = 85

# Lista para guardar los paquetes modificados
paquetes_modificados = []

# Iterar sobre los paquetes
for paquete in paquetes:
    # Verificar si el paquete tiene la capa Raw y contiene datos
    if paquete.haslayer(Raw) and paquete[Raw].load:
        # Verificar si contiene la cadena específica
        if b'SSH-2.0-OpenSSH_8.3p1 Ubuntu-1ubuntu0.1' in paquete[Raw].load:
            # Verificar si la dirección IP coincide
            if paquete[IP].src == ip_cliente:
                # Modificar la carga útil
                paquete[Raw].load = paquete[Raw].load.replace(
                    b'SSH-2.0-OpenSSH_8.3p1 Ubuntu-1ubuntu0.1',
                    b'SSH-2.0-OpenSSH_?'
                )

                # Ajustar el tamaño del paquete a 85 bytes
                payload = paquete[Raw].load
                if len(payload) > tamaño_deseado:
                    paquete[Raw].load = payload[:tamaño_deseado]
                else:
                    paquete[Raw].load = payload.ljust(tamaño_deseado, b'\x00')

                # Eliminar campos que deben recalcularse
                del paquete[IP].len
                del paquete[IP].chksum
                if paquete.haslayer(TCP):
                    del paquete[TCP].chksum

    # Agregar el paquete (modificado o no) a la lista
    paquetes_modificados.append(paquete)

# Escribir los paquetes modificados en el archivo de salida
wrpcap(pcap_mod, paquetes_modificados)
