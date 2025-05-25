import pygame
from settings import MAP_HEIGHT, MAP_WIDTH, FPS
from bird import Bird
from pipe import Pipe
from db import write_highscore, read_highscore

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        self.clock = pygame.time.Clock()
        self.pipe = Pipe()
        self.bird = Bird(150, MAP_HEIGHT // 2)
        self.score = 0
        self.current_highscore = read_highscore()
        self.run = True
        self.font = pygame.font.Font(None, 36)

    def draw_text(self, text, location):
        text_font = self.font.render(str(text), True, (255, 255, 255))
        self.win.blit(text_font, location)

    def draw_highscore(self, text, top_right_pos):
        text_surf = self.font.render(str(text), True, (255, 255, 255))
        text_rect = text_surf.get_rect()
        text_rect.topright = top_right_pos
        self.win.blit(text_surf, text_rect)

    def update_time(self, time):
        return round(time + 1 / FPS, 2)

    def update(self):
        self.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.jump()
            if event.type == pygame.QUIT:
                self.run = False

        if self.pipe.can_move():
            self.pipe.move()
        else:
            self.pipe = Pipe()

        self.bird.move()
        self.score = self.update_time(self.score)
        write_highscore(self.score)

        if self.bird.out_of_map() or self.pipe.collides_with_bird(self.bird):
            self.run = False

    def draw(self):
        self.win.fill((0, 0, 0))
        self.pipe.draw(self.win)
        self.bird.draw(self.win)
        self.draw_text(self.score, (10, 10))
        self.draw_highscore(f"Highscore: {self.current_highscore}", (MAP_WIDTH - 10, 10))
        pygame.display.update()

    def run_game(self):
        while self.run:
            self.update()
            self.draw()

        pygame.quit()
        #while not self.run:
        #    for event in pygame.event.get():
        #        if event.type == pygame.QUIT:
        #            pygame.quit()
        #            return

game = Game()
game.run_game()