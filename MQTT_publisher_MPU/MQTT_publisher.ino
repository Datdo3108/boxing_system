#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <MPU6050_light.h>

/* MQTT INIT*/
// WiFi credentials
const char* ssid = "Fpt5g";
const char* password = "04082001";

// HiveMQ credentials
const char* mqtt_server = "mqtt-dashboard.com";
const int mqtt_port = 8884;
const char* mqtt_user = "admin";
const char* mqtt_password = "123456";

// MQTT topics
const char* axis_x_topic = "esp/axis_x";
const char* axis_y_topic = "esp/axix_y";
const char* led_topic = "esp/led/state";;

// WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);

/* Sensor INIT*/
MPU6050 mpu(Wire);


// Function to connect to WiFi network
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

// Function to reconnect to MQTT broker
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "clientId-0W38dKNT56";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      //      client.publish("EFG", "hello world");
      // ... and resubscribe
      client.subscribe("esp/#");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
// Function to handle incoming MQTT messages
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  // Convert payload to string
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  // Print message
  Serial.println(message);

  // // Check if the topic is the LED topic
  // if (String(topic) == led_topic) {
  //   // Check the message and set the LED state accordingly
  //   if (message == "ON") {
  //     digitalWrite(LEDPIN, HIGH);
  //   } else if (message == "OFF") {
  //     digitalWrite(LEDPIN, LOW);
  //   }
  // }
}

void setup() {
  // Initialize serial port
  Serial.begin(115200);

  // Initialize sensor
  Wire.begin();
  mpu.begin();

  // Connect to WiFi network
  setup_wifi();

  // Set MQTT server, port and callback function
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {

  // Reconnect to MQTT broker if not connected
  if (!client.connected()) {
    reconnect();
  }

  // Process incoming MQTT messages
  client.loop();

  // Read sensor
  float axis_x = mpu.getAngleX();
  float axis_y = mpu.getAngleY();

  // Check if any reads failed and exit early (to try again).
  if (isnan(axis_x) || isnan(axis_y)) {
    Serial.println("Failed to read from sensor!");
    return;
  }

  // Print sensor values
  Serial.print("Accelerometer: x,y respectively ");
  Serial.print('\n');
  Serial.print(axis_x);
  Serial.print('\n');
  Serial.print(axis_y);

   // Convert sensor values to strings
   String axis_x_str = String(axis_x);
   String axis_y_str = String(axis_y);

   // Publish sensor values to MQTT topics
   client.publish(axis_x_topic, axis_x_str.c_str());
   client.publish(axis_y_topic, axis_y_str.c_str());

   // Wait for a second before next reading
   delay(1000);
}
