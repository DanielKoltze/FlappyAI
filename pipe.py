import random
import pygame
from settings import MAP_HEIGHT, MAP_WIDTH, MAX_PIPE_HEIGHT, MIN_PIPE_HEIGHT, MAX_PIPE_WIDTH, MIN_PIPE_WIDTH, MIN_PIPE_GAP, MAX_PIPE_GAP

class Pipe:
    def __init__(self, height=0, width=0, gap=0):
        if height == 0:
            height = random.randint(int(MAP_HEIGHT * MIN_PIPE_HEIGHT), int(MAP_HEIGHT * MAX_PIPE_HEIGHT))
        if width == 0:
            width = random.randint(int(MIN_PIPE_WIDTH), int(MAX_PIPE_WIDTH))
        if gap == 0:
            gap = random.randint(int(MIN_PIPE_GAP), int(MAX_PIPE_GAP))
        self.height = height
        self.width = width
        self.gap = gap
        self.x = MAP_WIDTH
        self.y = 0

    def move(self):
        self.x -= 10

    def draw(self, win):
        # bottom pipe
        pygame.draw.rect(win, (255, 0, 0), (self.x, MAP_HEIGHT - self.height, self.width, self.height))
        # top pipe
        top_height = MAP_HEIGHT - self.height - self.gap
        pygame.draw.rect(win, (255, 0, 0), (self.x, 0, self.width, top_height))

    def can_move(self):
        return self.x + self.width >= 0

    def collides_with_bird(self, bird):
        bottom_pipe_rect = pygame.Rect(self.x, MAP_HEIGHT - self.height, self.width, self.height)
        top_pipe_height = MAP_HEIGHT - self.height - self.gap
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, top_pipe_height)
        return bird.rect.colliderect(bottom_pipe_rect) or bird.rect.colliderect(top_pipe_rect)
