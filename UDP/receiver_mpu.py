import socket
import matplotlib.pyplot as plt
import numpy as np
import time

localIP = "0.0.0.0"  # Listen on all available network interfaces
localPort = 1234    # Replace with the same port number used on the ESP8266
bufferSize = 1024

## Set up plotting
plt.ion()  # Enable interactive mode for real-time plotting
t_data = []
x_data = []
y_data = []
z_data = []

fig, ax = plt.subplots()
line, = ax.plot(t_data, y_data)
ax.set_xlabel("Time")
ax.set_ylabel("Data Unit")
ax.set_title("Real-time Flow Data")
cTime_0 = time.time()


# Create a UDP socket
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the specified IP address and port
udpSocket.bind((localIP, localPort))

print("UDP server listening")

try:
    # Continuously listen for incoming UDP packets
    while True:
        bytesReceived, senderAddress = udpSocket.recvfrom(bufferSize)
        dataReceived = bytesReceived.decode("utf-8")
        
        # Process incoming UDP packets
        print(f"Received data: {dataReceived}, type: {type(dataReceived)}")
        x, y, z = [float(i) for i in dataReceived.split(";")]

        cTime = time.time() - cTime_0

        # Real-time plotting
        x_data.append(x)
        y_data.append(y)
        z_data.append(z)
        t_data.append(cTime)

        # Update the line chart
        # line.set_xdata(t_data)
        # line.set_ydata(x_data)
        # line.set_ydata(y_data)
        # line.set_ydata(_data)
        # Plot data
        plt.plot(t_data, x_data)
        plt.plot(t_data, y_data)
        plt.plot(t_data, z_data)
        
        ax.relim()
        ax.autoscale_view()

        plt.draw()
        plt.pause(0.001)  # Pause for a short time to update the plot

except KeyboardInterrupt:
    # Close the UDP socket when a keyboard interrupt occurs
    udpSocket.close()
    print("UDP socket closed")