import matplotlib.pyplot as plt
import numpy as np

def plot(data):
    plt.ion()  # Enable interactive mode for real-time plotting

    x_data = []
    y_data = []

fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data)

ax.set_xlabel("Time")
ax.set_ylabel("Data Unit")
ax.set_title("Real-time Flow Data")

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
plt.pause(0.001)  # Pause for a short time to update the plot