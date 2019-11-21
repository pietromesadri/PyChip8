import pygame

class Renderer:
    pygame.display.init()

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    def clear_screen(self, r=0, g=0, b=0):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((r, g, b))
        self.screen.blit(background, (0,0))
        pygame.display.flip()