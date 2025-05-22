# zmq_handler.py
# ZMQ 통신 처리
import zmq      #ZeroMQ(ZMQ) 라이브러리를 임포트, 고성능 비동기 메시징 라이브러리로, 다양한 통신 패턴(PUB/SUB, REQ/REP 등)을 지원

#ZMQ 구독자(Subscriber)를 설정하고 반환하는 함수 정의
def setup_subscriber():
    context = zmq.Context()     #ZMQ 통신의 기본 단위인 컨텍스트 객체를 생성
    sub_socket = context.socket(zmq.SUB)        #zmq.SUB 타입의 소켓을 생성
    sub_socket.connect("tcp://localhost:6000")  #로컬호스트(localhost)의 6000번 포트로 연결, 퍼블리셔 코드에서 pub_socket.bind("tcp://*:6000")로 열려 있어 연결이 가능
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, "") #구독 필터를 설정.빈 문자열 ""은 모든 주제(topic)의 메시지를 구독
    return sub_socket