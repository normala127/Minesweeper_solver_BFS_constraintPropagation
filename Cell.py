import pygame
from Settings import *

class Cell:
    def __init__(self, x, y, state, visability=False, image, flagged=False):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.image=image
        self.cell_state = state
        self.cell_visability = visability

#possible_states = {"Mine": -1, "Safe": 0, "Number": 1, "Not shown": 'N',}
#cell_hidden = 'N'