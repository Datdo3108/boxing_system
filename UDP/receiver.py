import socket
import matplotlib.pyplot as plt
import numpy as np

localIP = "0.0.0.0"  # Listen on all available network interfaces
localPort = 1234    # Replace with the same port number used on the ESP8266
bufferSize = 1024

## Set up plotting
plt.ion()  # Enable interactive mode for real-time plotting
x_data = []
y_data = []
fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data)
ax.set_xlabel("Time")
ax.set_ylabel("Data Unit")
ax.set_title("Real-time Flow Data")


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
        print("Received data:", dataReceived)
        dataReceived = float(dataReceived)
        print("Received data:", dataReceived)
        print("Data type: ", type(dataReceived))

        # Real-time plotting
        y_data.append(dataReceived)
        x_data.append(len(y_data))

        # Update the line chart
        line.set_xdata(x_data)
        line.set_ydata(y_data)
        ax.relim()
        ax.autoscale_view()

        plt.draw()
        plt.pause(0.001)  # Pause for a short time to update the plot

except KeyboardInterrupt:
    # Close the UDP socket when a keyboard interrupt occurs
    udpSocket.close()
    print("UDP socket closed")