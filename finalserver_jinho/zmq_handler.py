import zmq

def setup_subscriber():
    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://localhost:6000")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
    return sub_socket
