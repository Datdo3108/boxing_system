#include <ESP8266WiFi.h>
#include <HX711_ADC.h> // https://github.com/olkal/HX711_ADC
#include <Wire.h>
#include <stdio.h>
#include <stdlib.h>

const int rate = 500 // rate in milliseconds

const char* ssid = "LAPTOP-IO4BI4LC 0162";
const char* password = "lam123456";

const char* serverIP = "192.168.137.1";
const int serverPort = 1234;

HX711_ADC LoadCell(4, 5); // parameters: dt pin, sck pin<span data-mce-type="bookmark" style="display: inline-block; width: 0px; overflow: hidden; line-height: 0;" class="mce_SELRES_start"></span>

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    }
    Serial.println("Connected");

    LoadCell.begin(); // start connection to HX711
    LoadCell.start(2000); // load cells gets 2000ms of time to stabilize
    LoadCell.setCalFactor(10000);
}

void loop() {
    if (WiFi.status() == WL_CONNECTED) {
        WiFiClient client;

        if (!client.connect(serverIP, serverPort)) {
            Serial.println("Connection failed.");
            delay(2000);
            return;
        }

        while (1) {
            LoadCell.update(); // retrieves data from the load cell
            float x = LoadCell.getData(); // get output value
            Serial.println(i);

            // Send via TCP
            String message = String(x);
            client.print(message);
            Serial.println("Message sent to server");
            delay(rate);
        }
        

    }
}
