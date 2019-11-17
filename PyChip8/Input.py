import pygame

class Input:
    def __init__(self):
        self.key_down = 0
        self.key_pressed = ""

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.key_down = 1
                self.key_pressed = str(event.key)
                if event.key == pygame.K_q:
                    self.key_pressed = "q"
                    pygame.quit()
                    return 0
        return 1