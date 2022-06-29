
import pygame, sys 



pygame.init()

pygame.font.init()
from constants import WIN_SIZE, WIN_H, WIN_W, START_VEL 
from game_state import STATE


from handlers import handle_events
from draw import redraw_window
from client import Network




def main(name):
    cl = pygame.time.Clock()

    s = Network()
    STATE.current_id = s.connect(name)


    r_data = s.send({"cmd": "get"})


    STATE.users = r_data["users"]
    STATE.balls = r_data["balls"]

    print(r_data["users"])

    # crear ventana
    screen = pygame.display.set_mode(WIN_SIZE)

    while STATE.goOn:
        cl.tick(30)
        current_user = STATE.users[STATE.current_id]

        STATE.score = current_user["score"] 

        vel = START_VEL - round(STATE.score / 4)
        if vel < 10:
            vel = 10


        ### MOUSE HANDLER ###
        # dX, dY = pygame.mouse.get_pos()
        # # Find the angle from the center of the screen to the mouse in radians [-Pi, Pi]
        # rotation = math.atan2(
        #     dY - float(WIN_H) / 2, dX - float(WIN_W) / 2
        # )
        # # Convert radians to degrees [-180, 180]
        # rotation *= 180 / math.pi
        # # Normalize to [-1, 1]
        # # First project the point from unit circle to X-axis
        # # Then map resulting interval to [-1, 1]
        # normalized = (90 - math.fabs(rotation)) / 90
        # vx = vel * normalized
        # vy = 0
        # if rotation < 0:
        #     vy = - vel + math.fabs(vx)
        # else:
        #     vy = vel - math.fabs(vx)
        # tmpX = current_user["x"] + vx
        # tmpY = current_user["x"] + vy
        # current_user["x"] = tmpX
        # current_user["x"] = tmpY


        keys = pygame.key.get_pressed()
        PLAYER_RADIUS = current_user["r"]
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if current_user["x"] - vel - PLAYER_RADIUS  >= 0:
                current_user["x"] = current_user["x"] - vel

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if current_user["x"] + vel + PLAYER_RADIUS  <= WIN_W:
                current_user["x"] = current_user["x"] + vel

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if current_user["y"] - vel - PLAYER_RADIUS  >= 0:
                current_user["y"] = current_user["y"] - vel

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if current_user["y"] + vel + PLAYER_RADIUS  <= WIN_H:
                current_user["y"] = current_user["y"] + vel


        # data = "move " + str(current_user["x"]) + " " + str(current_user["y"])
        send_data = {
            "cmd": "move",
            "x": current_user["x"],
            "y": current_user["y"],
        }

        r_data = s.send(send_data)
        STATE.users = r_data["users"]
        STATE.balls = r_data["balls"]




        for event in pygame.event.get():
            handle_events(event)

        redraw_window(screen=screen)
        pygame.display.update()

    pygame.display.quit()
    pygame.quit()
    s.disconnect()
    sys.exit()


if __name__ == "__main__":
    print("hhehe")
    name = input("Name: ")
    main(name)
