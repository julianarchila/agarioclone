import socket

from _thread import *

from user_thread import user_thread
from server_state import STATE




def main():
    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set constants
    PORT = 5555

    HOST_NAME = socket.gethostname()
    SERVER_IP = socket.gethostbyname(HOST_NAME)

    # try to connect to server
    try:
        S.bind(('0.0.0.0', PORT))
    except socket.error as e:
        print(str(e))
        print("[SERVER] Server could not start")
        quit()

    S.listen()  # listen for connections

    print(f"[SERVER] Server Started with local ip {SERVER_IP}")

    while True:
        host, addr = S.accept()

        print("[CONNECTION] Connected to:", addr)

        # start game when a client on the server computer connects
        if not (STATE.start):
            STATE.start = True
            print("[STARTED] Game Started")

        start_new_thread(user_thread, (host, id))
        STATE.connections += 1




if __name__ == "__main__":
    main()
