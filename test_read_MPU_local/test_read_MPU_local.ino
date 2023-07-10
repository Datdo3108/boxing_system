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

  float x, y, z;

  // Set values to send
  x = mpu.getAngleX();
  y = mpu.getAngleY();
  z = mpu.getAngleZ();

  Serial.printf("%f,", x);
  Serial.printf("%f,", y);
  Serial.printf("%f\n", z);
  
  delay(10);
}
