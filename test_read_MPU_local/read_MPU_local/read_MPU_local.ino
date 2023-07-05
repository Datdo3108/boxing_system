#include <Wire.h>
#include <MPU6050_light.h>

MPU6050 mpu(Wire);
 
void setup() {
  // Init Serial Monitor
  Serial.begin(115200);
  Wire.begin();
  mpu.begin();

}
 
void loop() {
  mpu.update();

  float axis_x, axis_y, axis_z;

  // Set values to send
  axis_x = mpu.getAngleX();
  axis_y = mpu.getAngleY();
  axis_z = mpu.getAngleZ();

  Serial.print("Accelerometer: x,y,z respectively ");
  Serial.print('\n');
  Serial.print(axis_x);
  Serial.print('\n');
  Serial.print(axis_y);
  Serial.print('\n');
  Serial.print(axis_z);
  
  delay(1000);
}