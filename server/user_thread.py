# Utils
from socket import socket
import random, sys
from time import time
import time
import json


# My stuff
from gf import gen_user, gen_balls, serialize_state, check_collision, player_collision
from server_state import STATE


def user_thread(conn: socket, _id: any):
    """
    Every connection runs in a new thread where
    all the interactions with the server are handled
    """

    data = conn.recv(16)
    name = data.decode("utf-8")


    user = gen_user(name)
    conn.send(str.encode(user.id))


    STATE.users[user.id] = user

    print("Check 1")
    while True:
        try:
            # recieve data
            data = conn.recv(2048 * 4)
            if not data:
                break

            # unpickle data
            try:
                data = json.loads(data)
            except Exception as e:
                print("Error loading json")
                print(f"{data=}")
                print(e)


            # update user
            if data["cmd"] == "move":
                STATE.users[user.id].x = data["x"]
                STATE.users[user.id].y = data["y"]

                if STATE.start:
                    try:
                        check_collision()
                    except Exception as e:
                        print("Error checking collision")
                        print(e)

                    try:
                        player_collision()

                    except Exception as e:
                        print("Error checking player collision")
                        print(e)


            
            # if the amount of balls is less than 150 create more
            if len(STATE.balls) < 50:
                gen_balls(random.randrange(30,50))
                print("[GAME] Generating more orbs")


            if data["cmd"] == "get":
                print("Getter")


            send_data = json.dumps(serialize_state()).encode("utf-8")

            size = sys.getsizeof(send_data)

            conn.send(str.encode(str(size)))

            


            conn.send(send_data)


        except Exception as e:
            print(f"Error handling data from {_id}:\n{e}\n")
            break
        time.sleep(0.001)
    print("Check 2")

    print(f"DISCONNECTED: {_id}")
    conn.close()
    STATE.users.pop(user.id)
    STATE.connections -= 1
