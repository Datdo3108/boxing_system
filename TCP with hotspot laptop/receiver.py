import socket
import matplotlib.pyplot as plt
import numpy as np

HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 1234
RATE_SIZE = 4

plt.ion()  # Enable interactive mode for real-time plotting

x_data = []
y_data = []

fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data)

ax.set_xlabel("Time")
ax.set_ylabel("Data Unit")
ax.set_title("Real-time Flow Data")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    # with conn:
    print("Connected by", addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break

        data = float(data.decode())
        print("Received data:", data)
        print("Data type: ", type(data))

        y_data.append(data)
        x_data.append(len(y_data))

        # Update the line chart
        line.set_xdata(x_data)
        line.set_ydata(y_data)
        ax.relim()
        ax.autoscale_view()

        plt.draw()
        plt.pause(0.5)  # Pause for a short time to update the plot