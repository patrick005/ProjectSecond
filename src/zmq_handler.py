# zmq_handler.py - ZMQ 서브스크라이버 설정 모듈
import zmq

def setup_publisher():
    """
    ZMQ PUB 소켓을 설정하고 반환합니다.
    (현재 main.py와 relay_server.py에서 각각 바인딩하므로 사용되지 않을 수 있습니다.)
    """
    context = zmq.Context()
    publisher_socket = context.socket(zmq.PUB)
    return publisher_socket

def setup_subscriber():
    """
    ZMQ SUB 소켓을 설정하고 main.py에 반환합니다.
    main.py는 relay_server.py로부터 액션 메시지를 받습니다.
    """
    context = zmq.Context()
    subscriber_socket = context.socket(zmq.SUB)
    # relay_server.py의 PUB 소켓에 연결
    subscriber_socket.connect("tcp://localhost:6000") 
    # 모든 메시지를 구독 (접두사 필터링 없음)
    subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, "") 
    return subscriber_socket

if __name__ == '__main__':
    # 이 파일이 직접 실행될 때는 아무것도 하지 않음 (모듈로 임포트되어 사용)
    print("This file is meant to be imported as a module.")
    print("It provides ZMQ socket setup functions.")
