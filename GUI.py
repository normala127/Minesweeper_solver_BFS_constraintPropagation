import pygame
from Settings import *
from Board import *
from Solver import *


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self):
        self.board = Solver()
        self.board.start_game()
        self.board.solve(self.screen)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        else:
            self.end_screen()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.board.draw(self.screen)
        pygame.display.flip()

    def end_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)


game = Game()
while True:
    game.new()
    game.run()

# TODO da nekako ispise ako je win ili lose
# TODO code cleanup as i write the report