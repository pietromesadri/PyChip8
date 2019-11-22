import pygame

class Renderer:
    pygame.display.init()
    pygame.mixer.init()

    def __init__(self, width, height, pixel_size):
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.screen = pygame.display.set_mode((self.width*self.pixel_size, self.height*self.pixel_size))
        pygame.display.set_caption("PyChip-8 Emulator")
        self.sound = pygame.mixer.Sound("Beep.ogg")
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()

    def clear_screen(self, r=0, g=0, b=0):
        self.background.fill((r, g, b))
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

    def draw_graphics(self, gfx, color, bg_color = (0,0,0)):
        clr = color
        self.background.fill(bg_color)
        i = 0
        for y in range(int(self.height)):
            for x in range(int(self.width)):
                if gfx[i] == 1:
                    clr = color
                else:
                   clr = bg_color
                pygame.draw.rect(self.background, clr, \
                        ((x*self.pixel_size, y*self.pixel_size), \
                        (self.pixel_size, self.pixel_size))) 
                i += 1
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()


                
                        
