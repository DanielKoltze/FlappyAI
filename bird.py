from settings import VELOCITY, GRAVITY, MAP_HEIGHT, PLANE_PATH, PLANE_SIZE
import pygame

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.size = PLANE_SIZE
        self.image = pygame.image.load(PLANE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    def jump(self):
        self.vel = VELOCITY

    def move(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.center = (self.x, int(self.y))

    def draw(self, win):
        win.blit(self.image, self.rect)

    def out_of_map(self):
        return self.y - self.size < 0 or self.y + self.size > MAP_HEIGHT
