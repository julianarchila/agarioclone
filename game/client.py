import  sys
import _pickle as pickle
import json

import websocket


class Network:
    """
    class to connect, send and recieve information from the server

    need to hardcode the host attirbute to be the server's ip
    """

    def __init__(self):
        # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = websocket.WebSocket()
        # self.client.settimeout(10.0)
        # self.host = "127.0.0.1"
        self.host = "13.71.64.234"
        self.port = 5555
        # self.addr = (self.host, self.port)

        self.addr = f"ws://{self.host}:{self.port}"

    def connect(self, name):
        """
        connects to server and returns the id of the client that connected
        :param name: str
        :return: int reprsenting id
        """

        self.client.connect(self.addr)
        self.client.send(name)
        c_id = self.client.recv()

        if type(c_id) == bytes:
            c_id = c_id.decode("utf-8")

        print(f"Val recieved connecting: {c_id}")
        return c_id

        # self.client.connect(self.addr)
        # self.client.send(str.encode(name))
        # val = self.client.recv(128).decode("utf-8")
        # print(f"Val recieved connecting: {val}")
        # return val

    def disconnect(self):
        """
        disconnects from the server
        :return: None
        """
        self.client.close()

    def send(self, data, j=True):
        """
        sends information to the server

        :param data: str
        :param pick: boolean if should pickle or not
        :return: str
        """
        try:
            if j:
                self.client.send(json.dumps(data))
            else:
                self.client.send(data)

            # reply = self.client.recv(int(size.decode()))
            reply = self.client.recv()

            try:
                reply = json.loads(reply)
            except Exception as e:
                print("Error loading json", "-"*20)
                print(f"reply: {reply}")
                print("Error loading json", "-"*20)
                print(e)

            return reply
        except Exception as e:
            print(e)
