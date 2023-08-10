import socket
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
import csv

localIP = "0.0.0.0"  # Listen on all available network interfaces
localPort = 1234    # Replace with the same port number used on the ESP8266
bufferSize = 1024

# Create a UDP socket
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the specified IP address and port
udpSocket.bind((localIP, localPort))

print("UDP server listening")
count = 0
cTime_0 = time.time()

data_list = []
time_data = []

# Continuously listen for incoming UDP packets
while True:
    bytesReceived, senderAddress = udpSocket.recvfrom(bufferSize)
    dataReceived = bytesReceived.decode("utf-8")
    cTime = time.time() - cTime_0

    # Process incoming UDP packets
    # print(f"Received data: {dataReceived}, type: {type(dataReceived)} -- {senderAddress}")
    count += 1
    print(count)
    dataReceived = list([dataReceived]) + list([senderAddress]) + list([cTime])
    print(dataReceived)
    # x, y, z = [float(i) for i in dataReceived.split(";")]
    data_list.append(dataReceived)

    time_data.append(cTime)

    if(cTime > 6):
        break


def write_to_csv(data, file_name):
    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        for row in data:
            csv_writer.writerow(row)

# write_to_csv(time_data, 'udp_time.csv')
write_to_csv(data_list, 'udp_data.csv')

# print(f"Data written to {csv_file_name}")
