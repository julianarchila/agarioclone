from utils import generate_random_color
import random
from constants import START_R
class User:
    def __init__(self, name, x, y, color, id) -> None:
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.id = id 
        self.r = START_R
        self.score = 0

    def serialize(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "r": self.r,
            "score": self.score,
            "name": self.name,
        }


class Ball:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.color = generate_random_color()
        self.r = random.randint(5, 10)

    def serialize(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "r": self.r,
        }