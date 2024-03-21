import sys
import socket
import time
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QElapsedTimer
import pyqtgraph as pg

from ui_form import UIForm

class UDPServer(QThread):
    data_received = pyqtSignal(str)
    data_to_save = pd.DataFrame()

    def __init__(self):
        super().__init__()
        self.server_socket = None
        self.running = False

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(("0.0.0.0", 1234))
        self.running = True

    def stop_server(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()

    def write_data_to_csv(self, timestamp, data, file_name):
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, data])

    def run(self):
        self.start_server()
        # data_to_save = pd.DataFrame()
        initial_time = time.time()
        list_dir = os.listdir(os.getcwd())
        file_name = 'ui_test.csv'
        if file_name in list_dir:
            os.remove(file_name)
        while self.running:
            data, _ = self.server_socket.recvfrom(1024)
            self.message = data.decode('utf-8')
            # timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            timestamp = time.time() - initial_time
            # self.data_received.emit(f"{timestamp}: {self.message}")
            # self.write_data_to_csv(timestamp, self.message, file_name)  # Write data to CSV
            # joint_data = list([timestamp]) + list([self.message])
            # data_to_save = pd.concat([data_to_save,pd.Series(joint_data)], axis = 1)
            # if timestamp > 3:
                # self.data_to_save = data_to_save.T
                # break

class AppMPU(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

        # Parameters for data
        self.update_time = 10           # in miliseconds
        self.display_length = 500
        self.marker_range = np.array([-33000, 33000])

        # Widgets for graphs
        self.mpu_x_graph = self.ui_form.mpu_x_graph
        self.mpu_y_graph = self.ui_form.mpu_y_graph
        self.mpu_z_graph = self.ui_form.mpu_z_graph
        self.mpu_x_graph.plot(np.array([0, self.update_time * self.display_length]), self.marker_range, pen=(255,255,255, 100))       
                                                                                                            # (255,255,255, 100): transparent color

        # Push button
        self.udp_start_button = self.ui_form.udp_start_button
        self.udp_start_button.clicked.connect(self.start_server)
        self.udp_stop_button = self.ui_form.udp_stop_button
        self.udp_stop_button.clicked.connect(self.stop_server)

        self.udp_server = UDPServer()

        self.button_flag = True

    def start_server(self):
        self.udp_start_button.setEnabled(False)
        self.udp_stop_button.setEnabled(True)
        self.udp_server.start()
        self.show_graph()

    def stop_server(self):
        self.udp_start_button.setEnabled(True)
        self.udp_stop_button.setEnabled(False)
        self.udp_server.stop_server()
        self.button_flag = False    # To stop graph

    def show_graph(self):
        self.button_flag = True
        self.mpu_x_graph.clear()
        self.mpu_x_marker = self.mpu_x_graph.plot(np.array([0, self.update_time * self.display_length]), self.marker_range, pen=(255,255,255, 100))

        self.mpu_time = np.array([0])
        self.mpu_x = np.array([0])

        self.plot_data()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(self.update_time)  # Update plot every 1000 milliseconds (1 second)

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()

    def plot_data(self):
        self.mpu_x_curve = self.mpu_x_graph.plot(self.mpu_time, self.mpu_x, pen='r')

    def update_plot(self):
        if self.button_flag == True:
            new_x = self.udp_server.message
            print(new_x)
            self.mpu_x = np.insert(self.mpu_x, len(self.mpu_x), new_x)

            new_time = self.elapsed_timer.elapsed()
            self.mpu_time = np.insert(self.mpu_time, len(self.mpu_time), new_time)

            if len(self.mpu_time) > self.display_length:
                self.mpu_time = np.delete(self.mpu_time, 0)
                self.mpu_x = np.delete(self.mpu_x, 0)
                self.mpu_x_marker.setData(np.array([self.mpu_time[0], self.mpu_time[-1]]), self.marker_range)
        self.mpu_x_curve.setData(self.mpu_time, self.mpu_x)
        

    def init_ui(self):
        # Create and set up the UI form
        self.ui_form = UIForm()
        self.setCentralWidget(self.ui_form)
        self.setWindowTitle('MPU App')

def main():
    app = QApplication(sys.argv)
    window = AppMPU()
    window.setWindowTitle("MPU6050 accelerometer App")
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
