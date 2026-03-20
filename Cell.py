import pygame
from Settings import *

class Cell:
    def __init__(self, x, y, state, image, visability=False, flagged=False):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.image=image
        self.cell_state = state
        self.cell_visability = visability
        self.flagged = flagged
    
    def draw(self, board_surface):
        pass

#possible_states = {"Mine": -1, "Safe": 0, "Number": 1, "Not shown": 'N',}
#cell_hidden = 'N'
#TODO svugdje gdje se zove cell moras promijenit parametre