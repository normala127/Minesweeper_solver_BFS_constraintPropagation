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
        self.draw()    
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
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 64, bold=True)
        small_font = pygame.font.SysFont("Arial", 28)

        if self.board.won:
            message = "You Won!"
            color = (0, 200, 0)      
        else:
            message = "You Lost!"
            color = (200, 0, 0)    

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return  

            self.screen.fill(BGCOLOR)
            self.board.draw(self.screen)  
            
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            
            text = font.render(message, True, color)
            self.screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
            
            sub = small_font.render("Press any key or click to play again", True, (255, 255, 255))
            self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

            pygame.display.flip()
            self.clock.tick(FPS)


game = Game()
while True:
    game.new()
    game.run()
