from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
import pyqtgraph as pg

class UIForm(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widget
        # Widget for graph
        self.mpu_x_graph = pg.PlotWidget(self)                          # MPU axis X
        self.mpu_x_graph.setGeometry(300, 0, 1500, 300)
        self.mpu_x_graph.setBackground('w')
        self.mpu_y_graph = pg.PlotWidget(self)                          # MPU axis Y
        self.mpu_y_graph.setGeometry(300, 300, 1500, 300)
        self.mpu_y_graph.setBackground('w')
        self.mpu_z_graph = pg.PlotWidget(self)                          # MPU axis Z
        self.mpu_z_graph.setGeometry(300, 600, 1500, 300)
        self.mpu_z_graph.setBackground('w')

        self.mpu_x_label = QLabel('MPU axis X', self)
        self.mpu_x_label.setGeometry(0, 0, 300, 300)
        self.mpu_x_label.setStyleSheet('background-color: green')
        self.mpu_x_label = QLabel('MPU axis Y', self)
        self.mpu_x_label.setGeometry(0, 300, 300, 300)
        self.mpu_x_label.setStyleSheet('background-color: green')
        self.mpu_x_label = QLabel('MPU axis Z', self)
        self.mpu_x_label.setGeometry(0, 600, 300, 300)
        self.mpu_x_label.setStyleSheet('background-color: green')

        # UDP widget
        self.udp_start_button = QPushButton('Start', self)
        self.udp_start_button.setGeometry(0, 900, 150, 30)
        self.udp_stop_button = QPushButton('Stop', self)
        self.udp_stop_button.setGeometry(150, 900, 150, 30)