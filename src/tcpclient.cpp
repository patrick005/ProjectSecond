#include <ESP8266WiFi.h>
#include <GPIO.h> // ESP8266 GPIO 라이브러리

// WiFi 네트워크 정보
#define WIFI_SSID "turtle"
#define WIFI_PASSWORD "turtlebot3"

// 서버 IP 주소 및 포트
const char* serverIP = "192.168.0.93";
const uint16_t serverPort = 7755;

// GPIO 핀 정의
const int attackButtonPin = D1;
const int moveButtonPin = D3;

const long sendInterval = 100; // 메시지 전송 간격 (ms)
unsigned long lastSendTime = 0;

WiFiClient client;
bool connectedToServer = false;
String myIP = "";

void setup() {
  Serial.begin(115200);
  Serial.println("\nESP8266 클라이언트 시작!");

  pinMode(attackButtonPin, INPUT_PULLUP); // 풀업 저항 활성화
  pinMode(moveButtonPin, INPUT_PULLUP);   // 풀업 저항 활성화

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("WiFi에 연결 중...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi 연결 완료!");
  Serial.print("IP 주소: ");
  Serial.println(WiFi.localIP());
  myIP = WiFi.localIP().toString(); // 접속 성공 시 자신의 IP 주소 저장

  // 서버 연결 시도
  Serial.print("서버에 연결 시도: ");
  Serial.print(serverIP);
  Serial.print(":");
  Serial.println(serverPort);
  if (client.connect(serverIP, serverPort)) {
    Serial.println("서버 연결 성공!");
    connectedToServer = true;
  } else {
    Serial.println("서버 연결 실패!");
  }
}

void loop() {
  unsigned long currentTime = millis();

  if (connectedToServer) {
    // 공격 버튼이 눌려 있고, 전송 간격이 지났으면 "ATTACK" 전송
    if (digitalRead(attackButtonPin) == LOW && currentTime - lastSendTime >= sendInterval) {
      Serial.println("공격 버튼 눌림 - ATTACK 전송!");
      sendToServer("ATTACK");
      lastSendTime = currentTime;
    }

    // 이동 버튼이 눌려 있고, 전송 간격이 지났으면 "MOVEMENT" 전송
    else if (digitalRead(moveButtonPin) == LOW && currentTime - lastSendTime >= sendInterval) {
      Serial.println("이동 버튼 눌림 - MOVEMENT 전송!");
      sendToServer("MOVEMENT");
      lastSendTime = currentTime;
    }
  } else {
    Serial.println("서버와 연결되지 않음. 재연결 시도...");
    if (client.connect(serverIP, serverPort)) {
      Serial.println("서버 재연결 성공!");
      connectedToServer = true;
      myIP = WiFi.localIP().toString(); // 재접속 성공 시 IP 주소 업데이트
    }
  }

  delay(10); // 짧은 루프 지연
}

void sendToServer(String data) {
  if (connectedToServer) {
    client.print(data);
  } else {
    Serial.println("서버에 연결되지 않아 데이터 전송 실패: " + data);
  }
}