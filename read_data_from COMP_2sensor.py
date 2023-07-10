import pandas as pd
# import matplotlib.pyplot as plt

def extract_data(csv_path, time_path):
    df_time = pd.read_csv(time_path)
    df = pd.read_csv(csv_path, sep=',')
    print(df)

    df_mpu = pd.DataFrame()
    df_loadcell = pd.DataFrame()

    for i in range(1,len(df)):
        u = df.iloc[i,0]
        u = [ord(c) for c in u]     # convert to ascii code
        u.pop(-1)
        u.pop(-1)
        u = [chr(c) for c in u]     # convert ascii code back to character
        u = ''.join(u)
        u = u.split(' ')
        if len(u) == 4 and u[0].find('MPU') != 0:
            joint_list = list([float(u[1])]) + list([float(u[2])]) + list([float(u[3])]) + list([float(df_time.iloc[i,0])])
            df_mpu = pd.concat([df_mpu, pd.Series(joint_list)], axis=1)
        if len(u) == 2 and u[0].find('Loadcell') != 0:
            joint_list = list([float(u[1])]) + list([float(df_time.iloc[i,0])])
            df_loadcell = pd.concat([df_loadcell, pd.Series(joint_list)], axis=1)

    df_mpu = df_mpu.T
    df_mpu.columns = ['x', 'y', 'z', 'time']
    df_mpu.to_csv("Data Record/mpu_data.csv")

    df_loadcell = df_loadcell.T
    df_loadcell.columns = ['force', 'time']
    df_loadcell.to_csv("Data Record/loadcell_data.csv")

    return df_mpu, df_loadcell

# csv_path_1 = "Data Record/com_1.csv"
# time_path_1 = "Data Record/real_time.csv"
#
# df_mpu, df_loadcell = extract_data(csv_path_1, time_path_1)

# df_loadcell = df_loadcell.T
# df_loadcell.columns = ['force', 'time']
# df_loadcell.to_csv("Data Record/loadcell_data.csv")

# print(df_mpu.describe())
# print(df_loadcell.describe())

# plt.plot(df_mpu['time'],df_mpu['x'],label='x angle')
# plt.plot(df_mpu['time'],df_mpu['y'],label='y angle')
# plt.plot(df_mpu['time'],df_mpu['z'])
# plt.plot(df_loadcell['time'],df_loadcell['force'])
#
# plt.show()
