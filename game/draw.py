import pygame, operator
from constants import COLORS, TIME_FONT, NAME_FONT
from game_state import STATE


def draw_players(screen):
    for p in sorted(STATE.users.values(), key=operator.itemgetter("score")):
        #     pygame.draw.circle(screen, YELLOW, (posx,posy), playerrad)
        pygame.draw.circle(
            screen,
            p["color"],
            (p["x"], p["y"]),
             p["r"]
        )
        text = NAME_FONT.render(p["name"], 1, (0,0,0))
        screen.blit(text, (p["x"] - text.get_width()/2, p["y"] - text.get_height()/2))

def draw_balls(screen):
    for ball in STATE.balls:
        pygame.draw.circle(
            screen,
            ball["color"],
            (ball["x"], ball["y"]),
            ball["r"]
        )


def draw_scoreboard(screen):
	text = TIME_FONT.render("Score: " + str(round(STATE.score)),1,(0,0,0))
	screen.blit(text,(10,15 + text.get_height()))



def draw_time(screen):
    pass


# pinta la pantalla de blanco y dibuja los jugadores
def redraw_window(screen):
    screen.fill(COLORS.white)

    draw_balls(screen)

    draw_players(screen)

    draw_scoreboard(screen=screen)

