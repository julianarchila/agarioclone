import random, math, operator
from utils import generate_id, calc_distance, generate_random_color
from models import User, Ball
from constants import WIN_H, WIN_W, B_N 
from server_state import STATE

def gen_start_location(r):
    """ 
    generates a random location and checks if it's not overlapping
    with any of the players or balls. if it is, it generates a new location
    """
    x = random.randint(0, WIN_W)
    y = random.randint(0, WIN_H)
    while True:
        for item in STATE.balls:
            if calc_distance(item.x,item.y, x, y) - ( item.r + r) < 0:
                continue

        for _, p in STATE.users.items():
            if calc_distance(p.x, p.y, x, y) - (p.r + r) < 0:
                continue

        break

    return x, y

def gen_user(name) -> User:
    random_color = generate_random_color()
    new_id = generate_id()
    new_user = User(name, 0, 0, random_color, new_id)
    (x,y) = gen_start_location(new_user.r)
    new_user.x = x
    new_user.y = y
    return new_user


def gen_balls(n: int = None) -> None:
    if n is None:
        n = B_N


    for _ in range(n):
        new_ball = Ball(0, 0)
        (x,y) = gen_start_location(new_ball.r)
        new_ball.x = x
        new_ball.y = y

        STATE.balls.append(new_ball)


def serialize_state() -> dict:
    data = {
        "users": {},
        "balls": [],
        "msg": "hi",
    }
    for _, user in STATE.users.items():
        data["users"][user.id] = user.serialize()

    for ball in STATE.balls:
        data["balls"].append(ball.serialize())

    return data


def check_collision():
    """
    checks if any of the player have collided with any of the balls

    :param players: a dictonary of players
    :param balls: a list of balls
    :return: None
    """
    for _, p in STATE.users.items():
        for ball in STATE.balls:
            dis = calc_distance(p.x, p.y, ball.x, ball.y)

            if dis <= p.r + ball.r:
                STATE.users[p.id].score += 0.5
                STATE.users[p.id].r += 0.5
                # p.score = p.score + 0.5
                STATE.balls.remove(ball)


def player_collision():
    """
    checks for player collision and handles that collision

    :param players: dict
    :return: None
    """
    sort_players = sorted(STATE.users.values(), key=operator.attrgetter('score'))
    for x, player1 in enumerate(sort_players):
        for player2 in sort_players[x+1:]:
            p1x = STATE.users[player1.id].x
            p1y = STATE.users[player1.id].y

            p2x = STATE.users[player2.id].x
            p2y = STATE.users[player2.id].y

            dis = math.sqrt((p1x - p2x)**2 + (p1y-p2y)**2)
            
            if dis < STATE.users[player2.id].score - STATE.users[player1.id].score *0.85:
                STATE.users[player2.id].score = math.sqrt(STATE.users[player2.id].score**2 + STATE.users[player1.id].score**2) # adding areas instead of radii
                STATE.users[player1.id].score = 0
                STATE.users[player1.id].x, STATE.users[player1.id].y = gen_start_location(STATE.users[player1.id].r)
                print(f"[GAME] " + STATE.users[player2.id].name + " ATE " + STATE.users[player1.id].name)


def new_check_player_collision():
    sorted_players = sorted(STATE.users.values(), key=operator.attrgetter('score'))
