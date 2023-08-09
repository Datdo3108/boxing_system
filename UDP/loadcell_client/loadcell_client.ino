#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <HX711_ADC.h> // https://github.com/olkal/HX711_ADC
#include <Wire.h>


const char* ssid = "LAPTOP-IO4BI4LC 0162";
const char* password = "lam123456";
const IPAddress laptopIP(192, 168, 137, 1);  // Replace with your laptop's IP address
const unsigned int laptopPort = 1234;        // Replace with the desired port number

const unsigned int localPort = 8888;  // Local port to listen on

WiFiUDP udp;
HX711_ADC LoadCell(4, 5); // parameters: dt pin, sck pin<span data-mce-type="bookmark" style="display: inline-block; width: 0px; overflow: hidden; line-height: 0;" class="mce_SELRES_start"></span>

void setup() {
    Serial.begin(115200);
    Wire.begin();
    LoadCell.begin(); // start connection to HX711
    LoadCell.start(2000); // load cells gets 2000ms of time to stabilize
    LoadCell.setCalFactor(10000);

    WiFi.begin(ssid, password);

    Serial.println("Connecting to WiFi");
        while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }

    Serial.println("Connected to WiFi");

    udp.begin(localPort);
}

void loop() {
    LoadCell.update(); // retrieves data from the load cell
    // Read your sensor data or prepare the data you want to send
    float x = LoadCell.getData(); // get output value   

    // Convert the sensor value to a string
    String dataToSend = String(x);

    // Send the data to the laptop
    udp.beginPacket(laptopIP, laptopPort);
    udp.write(dataToSend.c_str(), dataToSend.length());
    udp.endPacket();

    delay(10);  // Adjust the delay according to your requirements
}
