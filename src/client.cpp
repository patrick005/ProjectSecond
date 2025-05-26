// client.cpp - ESP8266 MPU6050 센서 데이터 전송 및 게임 상태 수신 클라이언트
// 이 코드는 NodeMCU 1.0 (ESP-12E Module) 보드를 기준으로 작성되었습니다.

// #include <Arduino.h>        // Arduino 기본 라이브러리
#include <ESP8266WiFi.h>     // ESP8266의 WiFi 기능 사용을 위한 라이브러리
#include <Adafruit_MPU6050.h> // MPU6050 센서 제어를 위한 Adafruit 라이브러리
#include <Adafruit_Sensor.h> // Adafruit 센서 통합 라이브러리
#include <Wire.h>            // I2C 통신을 위한 라이브러리 (MPU6050 통신에 사용)

// LED 핀 정의 (NodeMCU D6, D7, D8 핀 사용)
// Common Cathode (공통 캐소드) RGB LED를 가정합니다.
// HIGH 신호 인가 시 해당 색상 LED가 켜집니다.
#define RED_LED_PIN   D6 // GPIO12
#define GREEN_LED_PIN D7 // GPIO13
#define BLUE_LED_PIN  D8 // GPIO15

// WiFi 접속 정보
const char* ssid = "turtle";      // 접속할 WiFi 네트워크 이름
const char* password = "turtlebot3"; // 접속할 WiFi 네트워크 비밀번호

// 서버 (라즈베리파이) 정보
const char* serverIP = "192.168.0.43"; // 라즈베리파이의 고정 IP 주소 (환경에 맞게 변경 필요)
const int serverPort = 7755;           // 라즈베리파이의 TCP 중개 서버 포트

// MPU6050 센서 객체 생성
Adafruit_MPU6050 mpu;
// WiFiClient 객체 생성 (TCP 통신에 사용). 전역 변수로 선언하여 연결 유지
WiFiClient client;

// 게임 상태 관리 변수
bool gameStarted = false; // 현재 게임이 시작되었는지 여부를 나타내는 플래그 (서버로부터 수신)
                          // true: 게임 진행 중, false: 게임 대기 중

// 액션 감지 간격 및 마지막 액션 시간
unsigned long lastActionTime = 0;   // 마지막으로 액션을 전송한 시간 (ms)
unsigned long actionInterval = 200; // 액션 전송 최소 간격 (쿨타임, 200ms)
                                    // 200ms 이내에는 연속적인 액션 전송을 방지

// MPU6050 가속도 임계값 (힘껏 휘둘러야 인식될 정도로 빡빡하게 설정)
// 이 값은 실제 MPU6050의 출력값 (g 단위)을 기준으로 실험을 통해 조정될 수 있습니다.
float attackThresholdX = 15.0;  // X축 가속도 임계값 (ATTACK 판별 기준)
float movementThresholdY = 15.0; // Y축 가속도 임계값 (MOVEMENT 판별 기준)

/**
 * @brief LED 색상을 설정하는 함수 (공통 캐소드 타입 가정)
 * @param r 빨간색 밝기 (0: 꺼짐, 1~255: 켜짐 - 현재는 0 아니면 켜짐)
 * @param g 초록색 밝기
 * @param b 파란색 밝기
 * 공통 캐소드 LED는 HIGH 신호 인가 시 해당 색상 LED가 켜집니다.
 */
void setColor(uint8_t r, uint8_t g, uint8_t b) {
  digitalWrite(RED_LED_PIN,   r > 0 ? HIGH : LOW);
  digitalWrite(GREEN_LED_PIN, g > 0 ? HIGH : LOW);
  digitalWrite(BLUE_LED_PIN,  b > 0 ? HIGH : LOW);
}

/**
 * @brief 초기 설정 함수 (프로그램 시작 시 한 번 실행)
 * WiFi 연결, MPU6050 초기화, 서버 TCP 연결을 수행합니다.
 */
void setup() {
  // LED 핀들을 OUTPUT 모드로 설정
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(BLUE_LED_PIN, OUTPUT);
  setColor(0, 0, 0); // 모든 LED 초기화 (꺼짐)

  Serial.begin(115200); // 시리얼 통신 시작 (디버깅 출력용)
  Serial.println("MPU6050 TCP Client");

  // WiFi 연결 시도 및 LED 피드백
  setColor(0, 0, 255); // LED 파란불: WiFi 연결 시도 중
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) { // WiFi 연결 대기
    delay(500); // 0.5초 대기
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP()); // 할당받은 IP 주소 출력
  setColor(0, 255, 0); // LED 초록불: WiFi 연결 성공

  // MPU6050 센서 초기화
  // MPU6050이 발견되지 않으면 무한 대기 (치명적인 오류로 간주)
  if (!mpu.begin()) {
    Serial.println("MPU6050 not found");
    // 초기화 실패 시 시스템이 멈추도록 하여 문제 인지 가능
    while (1); 
  }
  Serial.println("MPU6050 initialized");
  // 가속도계 범위를 +-16G로 설정 (센서의 감도 설정)
  // 높은 임계값에 맞춰 더 넓은 측정 범위 사용
  mpu.setAccelerometerRange(MPU6050_RANGE_16_G); 

  // 서버에 TCP 연결 시도 (Setup에서 한 번만 시도)
  // 연결 실패 시 무한 대기하여 서버 연결 필수임을 강조
  if (!client.connect(serverIP, serverPort)) {
    Serial.println("TCP 연결 실패");
    setColor(255, 0, 0); // LED 빨간불: TCP 연결 실패
    // 초기 연결이 실패하면 시스템이 멈추도록 하여 문제 인지 가능
    while (1); 
  }
  Serial.println("서버에 TCP 연결 성공");
  // 서버 연결 성공 시 LED 초록불은 WiFi 연결 성공과 겹치므로 유지
  // setColor(0, 255, 0); 
}

/**
 * @brief 메인 루프 함수 (반복적으로 실행)
 * 서버로부터 게임 플래그 수신, MPU6050 데이터 읽기, 액션 감지 및 전송을 수행합니다.
 */
void loop() {
  // 1. 서버 연결 상태 확인 및 재연결 시도
  if (!client.connected()) {
    Serial.println("서버 연결 끊김. 재연결 시도...");
    setColor(255, 0, 0); // LED 빨간불: 연결 끊김
    if (client.connect(serverIP, serverPort)) {
      Serial.println("서버 재연결 성공.");
      setColor(0, 255, 0); // LED 초록불: 재연결 성공
      // 재연결 후 플래그가 다시 전송될 것이므로 gameStarted 상태는 서버에 동기화될 것임
    } else {
      Serial.println("재연결 실패. 재시도...");
      delay(1000); // 재연결 실패 시 1초 대기 후 다음 루프에서 다시 시도
      return; // 현재 루프를 종료하고 다음 루프에서 다시 시도
    }
  }

  // 2. 서버로부터 게임 상태 플래그 수신
  // client.available()은 수신 버퍼에 읽을 수 있는 바이트가 있는지 확인
  if (client.available()) {
    int flag = client.read(); // 1바이트 데이터(플래그) 읽기
    // 수신된 플래그가 1이면 gameStarted를 true로, 아니면 false로 설정
    gameStarted = (flag == 1); 
    Serial.printf("게임 상태 플래그 수신: %d\n", flag); // 수신된 플래그 출력

    // 플래그에 따른 LED 피드백 (게임 진행 중: 초록, 게임 대기 중: 파랑)
    if (gameStarted) {
      setColor(0, 255, 0); // LED 초록불: 게임 진행 중
    } else {
      setColor(0, 0, 255); // LED 파란불: 게임 대기 중
    }
  }

  // 3. MPU6050 센서 데이터 읽기
  sensors_event_t a, g, temp; // 가속도(a), 자이로(g), 온도(temp) 이벤트 구조체
  mpu.getEvent(&a, &g, &temp); // 센서에서 최신 측정값을 읽어 각 구조체에 저장

  // 가속도 값의 절대값 처리 (방향 불문 움직임 크기만 고려)
  float ax = abs(a.acceleration.x); // X축 가속도 절대값
  float ay = abs(a.acceleration.y); // Y축 가속도 절대값

  String dataToSend = ""; // 서버로 전송할 메시지 (기본값은 빈 문자열)
  unsigned long now = millis(); // 현재 시간 (ms)

  // 4. 액션 전송 쿨타임 검사
  // actionInterval 이내에는 새로운 액션을 전송하지 않음
  if (now - lastActionTime < actionInterval) {
    delay(10); // 짧은 지연
    return;    // 현재 루프를 종료하고 다음 루프로 넘어감
  }

  // 5. 게임 상태에 따른 액션 판정 및 메시지 구성
  if (gameStarted) { // 게임이 진행 중일 때만 ATTACK 또는 MOVEMENT 판정
    // X축 가속도가 임계값을 초과하면 ATTACK
    if (ax > attackThresholdX) {
      dataToSend = "ATTACK";
    } 
    // X축 가속도가 임계값 이하고 Y축 가속도가 임계값을 초과하면 MOVEMENT
    else if (ay > movementThresholdY) {
      dataToSend = "MOVEMENT";
    }
    // 이외의 경우에는 dataToSend가 빈 문자열로 유지되어 전송되지 않음
  } else { // 게임 대기 중일 때는 ACCEPT만 전송
    dataToSend = "ACCEPT";
  }

  // 6. 감지된 메시지가 있을 경우 서버로 전송
  // dataToSend.length() > 0: 전송할 메시지가 있는 경우
  // client.connected(): 서버와의 TCP 연결이 유효한 경우
  if (dataToSend.length() > 0 && client.connected()) {
    client.print(dataToSend); // 서버로 메시지 전송
    Serial.print("전송 데이터: ");
    Serial.println(dataToSend);
    lastActionTime = now; // 마지막 액션 전송 시간 업데이트 (쿨타임 시작)
  }

  delay(120); // 센서 폴링 및 루프 반복 간격 (약 120ms 지연)
}