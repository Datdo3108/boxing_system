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

  // Set values to send
  float x = mpu.getAngleX();
  float y = mpu.getAngleY();
  float z = mpu.getAngleZ();

  Serial.printf("%f,", x);
  Serial.printf("%f,", y);
  Serial.printf("%f\n", z);
  
  delay(10);
}
