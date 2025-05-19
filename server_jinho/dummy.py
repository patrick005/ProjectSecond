# dummy_sender.py
import zmq
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://localhost:7755")

while True:
    gx = random.uniform(-1.0, 0.0)
    gy = random.uniform(0.0, -1.0)
    gz = 0.0  # 무시
    msg = f"{gx:.2f},{gy:.2f},{gz:.2f}"
    socket.send_string(msg)
    time.sleep(0.05)
