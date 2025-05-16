# server.py
# 서버 코드
# 라즈베리파이에서 규모가 커지면 docker로 묶어서 배포를 염두해 둘 것
# 최종 디버깅이 끝나면 bash 파일에 넣어서 부팅시 서버 구동되게 지정할 것

# Raspberry Pi (receiver.py)
import zmq
import threading
import time

def process_data(device_id, data):
    """수신된 데이터를 처리하는 함수 (비동기 처리 예시)"""
    print(f"[{device_id}] Received: {data}")
    time.sleep(0.1) # 데이터 처리 시뮬레이션

def receiver():
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind("tcp://*:4796")

    while True:
        try:
            message = pull_socket.recv_json()
            device_id = message.get("device_id", "Unknown")
            data = message.get("data")
            if data:
                # 각 장치에서 받은 데이터를 별도의 스레드에서 처리 (비동기 처리)
                threading.Thread(target=process_data, args=(device_id, data)).start()
        except zmq.error.ContextTerminated:
            break
        except Exception as e:
            print(f"Error receiving data: {e}")

if __name__ == "__main__":
    receiver_thread = threading.Thread(target=receiver)
    receiver_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nReceiver stopped.")
    finally:
        context.term()