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
        if not self.flagged and self.cell_visability:
            board_surface.blit(self.image, (self.x, self.y))
        elif self.flagged and not self.cell_visability:
            board_surface.blit(tile_flag, (self.x, self.y))
        elif not self.cell_visability:
            board_surface.blit(tile_unknown, (self.x, self.y))

#possible_states = {"Mine": -1, "Safe": 0, "Number": 1, "Not shown": 'N',}
#y is the row, x is the column