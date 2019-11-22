import pygame

class Input:
    def __init__(self):
        self.key_down = 0
        self.key_pressed = 0
        self.key_map = [
            pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
            pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
            pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
            pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v,
            ]

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.key_down = 1

                for key in range(len(self.key_map)):
                    if event.key == self.key_map[key]:
                        self.key_pressed = key

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return 0
            if event.type == pygame.KEYUP:
                self.key_down = 0

                for key in range(len(self.key_map)):
                    if event.key == self.key_map[key]:
                        self.key_pressed = key
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
        return 1