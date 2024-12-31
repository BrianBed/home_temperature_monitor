#include <ESP8266WiFi.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// GPIO where the DS18B20 is connected to
const int oneWireBus = 4;

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);

// Pass our oneWire reference to Dallas Temperature sensor
DallasTemperature sensors(&oneWire);

// DHT22 setup
#define DHTPIN 14      // Pin connected to the DHT22 data pin (GPIO2)
#define DHTTYPE DHT22 // DHT 22 (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", -4 * 3600, 60000); // Time zone offset (0 for UTC), update interval of 60 seconds


// WiFi setup
const char* ssid = "";           // Replace with your WiFi SSID
const char* password = "";   // Replace with your WiFi password
const char* server_ip = ""; // Replace with the IP address of your server
const uint16_t server_port = 8080;        // Port number of the server

const String device_id = "office ";       // Unique identifier for each ESP8266 device

WiFiClient client;

float tempPrev = 0.0;
unsigned long epochTime;
unsigned long prevTime;

void setup() {
  Serial.begin(115200);
  dht.begin();  // Start the DHT22 sensor
  pinMode(LED_BUILTIN,OUTPUT);

    // Start the DS18B20 sensor
  sensors.begin();

wifi_connect();

  // Connect to the server

  //if (client.connect(server_ip, server_port)) {
  //  Serial.println("Connected to the server");
  //} else {
  //  Serial.println("Connection to server failed!");
  //}

    timeClient.begin();
   //timeClient.setTimeOffset(-3600);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED){
    wifi_connect();
  }

   timeClient.update();
     epochTime = timeClient.getEpochTime();

  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0);
  Serial.print("Outside temperature: ");
  Serial.print(temperatureC);
  Serial.println("ºC");

  // Read temperature and humidity from the DHT22
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  float hif = dht.computeHeatIndex(temperature, humidity);


  Serial.println( "Temp: " + String(temperature) + "  Prev: " + String (tempPrev) + "  heat index: " + String(hif));

 if (prevTime  > epochTime){
  prevTime = epochTime - 45;
 }
 // if (isnan(humidity) || isnan(temperature)) {
  //  Serial.println("Failed to read from DHT sensor!");
   // return;
 Serial.println("Epoch time: " + String(epochTime) + "  Previous Time: " + String(prevTime));
 if (epochTime >= (prevTime + 60)) {
  // Format data as a string with a unique device ID
  String data = device_id + ",Temp: " + String(temperature) + "C,Humidity: " + String(humidity) + "%,heat index: " + String(hif) + "C,Time: " + (timeClient.getFormattedTime());
  String data1 = "outside ,Temp: " + String(temperatureC) + "C,Humidity: " + "Null" + "%,heat index: " + "Null" + "C,Time: " + (timeClient.getFormattedTime());
  Serial.println(data);
  tempPrev = temperature;
  prevTime = epochTime;

  // Send data to the server
    if (client.connect(server_ip, server_port)) {
      Serial.println("connected to server");
    }
//client.connect(server_ip, server_port);
  if (client.connected()) {
    client.println(data);
    client.println(data1);
      digitalWrite(LED_BUILTIN,!digitalRead(LED_BUILTIN));
  } else {
    Serial.println("Disconnected from server, attempting to reconnect...");
    if (client.connect(server_ip, server_port)) {
      Serial.println("Reconnected to server");

    }
  }
 }
   // client.stop();
  delay(10000);  // Send data every 5 seconds
}

void wifi_connect(){
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
}

