import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('udp_data.csv')
df.columns = ['data','address','time']

client_1_address = df['address'].value_counts().index[0]
client_2_address = df['address'].value_counts().index[1]
client_3_address = df['address'].value_counts().index[2]


client_1 = df[df['address'] == client_1_address]['data'].astype(float)
client_2 = df[df['address'] == client_2_address]['data'].str.split(';',expand=True).astype(float)
client_3 = df[df['address'] == client_3_address]['data'].str.split(';',expand=True).astype(float)

client_1_time = df[df['address'] == client_1_address]['time']
client_2_time = df[df['address'] == client_2_address]['time']
client_3_time = df[df['address'] == client_3_address]['time']

print(df.shape[0])
print(client_1_address)
print(client_2)
print(client_3)

fig1 = plt.figure(figsize=(14, 7))
plt.plot(client_1_time,client_1)
plt.title('Loadcell value',fontsize=30,color='r')

fig2 = plt.figure(figsize=(14,7))
ax21 = fig2.add_subplot(131)
ax22 = fig2.add_subplot(132)
ax23 = fig2.add_subplot(133)

fig2.suptitle('MPU sensor',fontsize=30,color='r')
ax21.title.set_text('x angle')
ax22.title.set_text('y angle')
ax23.title.set_text('z angle')

ax21.plot(client_2_time,client_2.iloc[:,0])
ax22.plot(client_2_time,client_2.iloc[:,1])
ax23.plot(client_2_time,client_2.iloc[:,2])

fig3 = plt.figure(figsize=(14,7))
ax31 = fig3.add_subplot(131)
ax32 = fig3.add_subplot(132)
ax33 = fig3.add_subplot(133)

ax31.plot(client_3_time,client_3.iloc[:,0])
ax32.plot(client_3_time,client_3.iloc[:,1])
ax33.plot(client_3_time,client_3.iloc[:,2])

fig3.suptitle('Joint angles (camera)',fontsize=30,color='r')
ax31.title.set_text('Arm')
ax32.title.set_text('Wrist')
ax33.title.set_text('Shoulder')

plt.show()

