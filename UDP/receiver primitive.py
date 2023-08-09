import socket
import matplotlib.pyplot as plt
import numpy as np

localIP = "0.0.0.0"  # Listen on all available network interfaces
localPort = 1234    # Replace with the same port number used on the ESP8266
bufferSize = 1024

# Create a UDP socket
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the specified IP address and port
udpSocket.bind((localIP, localPort))

print("UDP server listening")

# Continuously listen for incoming UDP packets
while True:
    bytesReceived, senderAddress = udpSocket.recvfrom(bufferSize)
    dataReceived = bytesReceived.decode("utf-8")
    
    # Process incoming UDP packets
    print(f"Received data: {dataReceived}, type: {type(dataReceived)}")
    x, y, z = [float(i) for i in dataReceived.split(";")]