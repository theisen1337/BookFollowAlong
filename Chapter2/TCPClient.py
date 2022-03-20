"""

    Copyright Thomas T.
    All Rights reserved.


"""

import socket

HOST = "localhost"
PORT = 9999
DATA = "Medium pizza extra cheese."     # 25 bytes

def simple_tcp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data.
        sock.connect((HOST, PORT))

        # Send data encoded, sendall() is dirty lie.
        sock.send(DATA.encode())

        # Return data from the server and shut down
        rec = sock.recv(1024)
        #received = str(sock.recv(1024), "utf-8")

    print("\n\nSent from client:  {}".format(DATA))
    print("Received from server:  {}".format(str(rec, "utf-8") ))


if __name__ == '__main__':
    simple_tcp_client()