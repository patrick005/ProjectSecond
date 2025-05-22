# client_cli.py
#import zmq
#
#def run_cli_client():
#    try:
#        # ZeroMQ 컨텍스트 생성
#        context = zmq.Context()
#
#        # PULL 소켓에 연결 (서버의 PULL 소켓 주소 및 포트)
#        push_socket = context.socket(zmq.PUSH)
#        server_address = "tcp://192.168.0.43:5555"  # 서버의 PULL 소켓 주소와 포트
#        push_socket.connect(server_address)
#        print(f"CLI 클라이언트가 {server_address}에 연결되었습니다.")
#
#        while True:
#            try:
#                # CLI 입력 받기
#                input_data = input("자이로 데이터를 'gx,gy,gz' 형식으로 입력하세요 (종료: quit): ")
#
#                if input_data.lower() == 'quit':
#                    break
#
#                # 입력 형식 확인 및 전송
#                try:
#                    gx_str, gy_str, gz_str = input_data.split(',')
#                    gx = float(gx_str.strip())
#                    gy = float(gy_str.strip())
#                    gz = float(gz_str.strip())
#                    message = f"{gx},{gy},{gz}"
#                    push_socket.send_string(message)
#                    print(f"전송된 데이터: {message}")
#                except ValueError:
#                    print("잘못된 입력 형식입니다. 'gx,gy,gz' 형식으로 입력해주세요.")
#
#            except KeyboardInterrupt:
#                print("\n클라이언트 종료")
#                break
#
#        # 소켓 닫기 및 컨텍스트 종료
#        push_socket.close()
#        context.term()
#
#    except zmq.error.ZMQError as e:
#        print(f"ZeroMQ 에러 발생: {e}")
#    except Exception as e:
#        print(f"일반적인 에러 발생: {e}")
#
#if __name__ == "__main__":
#    run_cli_client()

import zmq
import sys

def run_cli_client(server_address):
    try:
        context = zmq.Context()
        push_socket = context.socket(zmq.PUSH)
        push_socket.connect(server_address)
        print(f"클라이언트가 {server_address}에 연결되었습니다.")

        while True:
            try:
                input_data = input("자이로 데이터 (gx,gy,gz)를 쉼표로 구분하여 입력하세요 (종료: q): ")
                if input_data.lower() == 'q':
                    break

                gx_str, gy_str, gz_str = input_data.split(',')
                gx = float(gx_str.strip())
                gy = float(gy_str.strip())
                gz = float(gz_str.strip())

                message = f"{gx},{gy},{gz}"
                push_socket.send_string(message)
                print(f"전송된 데이터: {message}")

            except ValueError:
                print("잘못된 입력 형식입니다. gx,gy,gz 형식으로 입력해주세요.")

        push_socket.close()
        context.term()
        print("클라이언트 종료.")

    except zmq.error.ZMQError as e:
        print(f"ZeroMQ 에러 발생: {e}")
    except Exception as e:
        print(f"일반적인 에러 발생: {e}")

if __name__ == "__main__":
    server_address = "tcp://192.168.0.43:7755"  # 서버의 PULL 소켓 주소와 동일해야 합니다.
    run_cli_client(server_address)