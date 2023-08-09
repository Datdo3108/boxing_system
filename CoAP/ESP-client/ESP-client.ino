#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <coap-simple.h>

const char* ssid = "VIETTEL2.0";
const char* password = "toikhongbiet";
const char* serverIP = "192.168.1.231";
const int serverPort = 5683;  // CoAP default port

// CoAP client response callback
void callback_response(CoapPacket &packet, IPAddress ip, int port);
// CoAP server endpoint url callback
void callback_hello(CoapPacket &packet, IPAddress ip, int port);

// UDP and CoAP class
// other initialize is "Coap coap(Udp, 512);"
// 2nd default parameter is COAP_BUF_MAX_SIZE(defaulit:128)
// For UDP fragmentation, it is good to set the maximum under
// 1280byte when using the internet connection.
WiFiUDP udp;
Coap coap(udp);

// CoAP server endpoint URL
void callback_hello(CoapPacket &packet, IPAddress ip, int port) {
  Serial.println("[Hello] Received");

  // Respond with "Hello, World!"
  coap.sendResponse(ip, port, packet.messageid, "Hello, World!");
}

// CoAP client response callback
void callback_response(CoapPacket &packet, IPAddress ip, int port) {
  Serial.println("[Coap Response got]");

  // Your existing code for handling the CoAP client response goes here...
}

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // add server url endpoints.
  // can add multiple endpoint urls.
  // exp) coap.server(callback_switch, "switch");
  //      coap.server(callback_env, "env/temp");
  //      coap.server(callback_env, "env/humidity");
  Serial.println("Setup Callback Hello");
  coap.server(callback_hello, "hello");

  // Client response callback.
  // This endpoint is single callback.
  Serial.println("Setup Response Callback");
  coap.response(callback_response);

  // Start coap server/client
  coap.start();
}

void loop() {
  delay(1000);
  coap.loop();
}
