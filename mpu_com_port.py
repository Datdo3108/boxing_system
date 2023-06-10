import pandas as pd
import time
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    print(port)
    print(desc)
    print(hwid)
    if desc.find("USB-SERIAL CH340") != -1:
        esp_server = port
    if desc.find("Silicon Labs CP210x USB to UART Bridge") != -1:
        esp_client = port

# serialPort = serial.Serial(port = esp_server, baudrate=115200,
#                            bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialPort = serial.Serial(port = esp_server, baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

angle_data = pd.DataFrame()
real_time = pd.DataFrame()
cTime_0 = time.time()
while(1):
    try:
        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()
            cTime = time.time() - cTime_0

            # Print the contents of the serial data
            print(serialString.decode('ASCII'))
            x = list([serialString.decode('Ascii')])
            angle_data = pd.concat([angle_data, pd.Series(x)], axis=1)
            real_time = pd.concat([real_time, pd.Series(cTime)])
            # angle_data = pd.concat([angle_data, pd.Series(cTime)], axis=1)
            # Tell the device connected over the serial port that we recevied the data!
            # The b at the beginning is used to indicate bytes!
            if(cTime > 2):
                break
    except KeyboardInterrupt:
        break

angle_data = angle_data.T
angle_data.to_csv("Data Record/com_1.csv", index=None,header=True)
real_time.to_csv("Data Record/real_time.csv", index=None,header=True)

df2 = pd.read_csv("Data Record/com_1.csv")
print(df2.describe())
df_time = pd.read_csv("Data Record/real_time.csv")
print(df_time.describe())

# print(df2.iloc[len(df2),0])
# print(df2.iloc[len])
# time = df2.iloc[len(df2) - 1,0]
# time_arduino = (int(df2.iloc[len(df2) - 1,1]) - int(df2.iloc[0,1]))/1000000
# sample_rate = len(df2)/(df2.iloc[len(df2)-1,0] - df2.iloc[0,0])
# print("Sample rate = ", sample_rate)
# print("Time = ", time)
# print("ArduinoTime = ", time_arduino)
