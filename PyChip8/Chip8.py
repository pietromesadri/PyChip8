import random

class chip8:
    def __init__(self, chip8_fontset):
        self.pc = 0x200
        self.opcode = 0
        self.I = 0
        self.sp = 0
        self.stack = []
        self.v_register = []
        self.memory = []
        self.fontset = chip8_fontset
        self.d_timer = 0
        self.s_timer = 0
        self.gfx = []
        self.draw_flag = False
        self.key = []
        self.sprite_addr = []
        
        self.v_register = []
        self.memory = []

        # create the memories
        for i in range(4096):
            self.memory.append(0)
        for i in range(64*32):
            self.gfx.append(0)
        for i in range(16):
            self.v_register.append(0)
            self.stack.append(0)
            self.key.append(0)

        for i in range(len(self.fontset)):
            self.memory[i] = self.fontset[i]

    def load_game(self, game):
        with open(game, "rb") as g:
            for b in enumerate(g.read()):
                self.memory[b[0] + 512] = b[1]
        return 1

    def  emulate_cycle(self, sound):
        # Fetch opcode
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]

        # Decode opcode
        tmp = self.opcode & 0xF000
        if tmp == 0x0000:
            if self.opcode & 0x000F == 0x0000:
                for i in range(64*32):
                    self.gfx.append(0)
                self.draw_flag = True
                self.pc += 2
            elif self.opcode & 0x000F == 0x000E:
                self.sp -= 1
                self.pc = self.stack[self.sp]
                self.pc += 2
            else:
                print("Unknown opcode {0}".format(self.opcode))
        elif tmp == 0x1000:
            self.pc = self.opcode & 0x0FFF
        elif tmp == 0x2000:
            self.stack[self.sp] = self.pc
            self.sp += 1
            self.pc = self.opcode & 0x0FFF
        elif tmp == 0x3000:
            if self.v_register[(self.opcode & 0x0F00) >> 8] == \
                (self.opcode & 0x00FF):
                self.pc += 4
            else:
                self.pc += 2
        elif tmp == 0x4000:
            if self.v_register[(self.opcode & 0x0F00) >> 8] != \
                (self.opcode & 0x00FF):
                self.pc += 4
            else:
                self.pc += 2
        elif tmp == 0x5000:
            if self.v_register[(self.opcode & 0x0F00) >> 8] == \
                self.v_register[(self.opcode & 0x00F0) >> 4]:
                self.pc += 4
            else:
                self.pc += 2
        elif tmp == 0x6000:
            self.v_register[(self.opcode & 0x0F00) >> 8] = self.opcode & 0x00FF
            self.pc += 2
        elif tmp == 0x7000:
            self.v_register[(self.opcode & 0x0F00) >> 8] += self.opcode & 0x00FF
            self.pc += 2
        elif tmp == 0x8000:
            if self.opcode & 0x000F == 0x0000:
                self.v_register[(self.opcode & 0x0F00) >> 8] = \
                    self.v_register[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
            elif self.opcode & 0x000F == 0x0001:
                self.v_register[(self.opcode & 0x0F00) >> 8] = \
                    self.v_register[(self.opcode & 0x0F00) >> 8] | \
                    self.v_register[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
            elif self.opcode & 0x000F == 0x0002:
                self.v_register[(self.opcode & 0x0F00) >> 8] = \
                    self.v_register[(self.opcode & 0x0F00) >> 8] & \
                    self.v_register[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
            elif self.opcode & 0x000F == 0x0003:
                self.v_register[(self.opcode & 0x0F00) >> 8] = \
                    self.v_register[(self.opcode & 0x0F00) >> 8] ^ \
                    self.v_register[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
            elif self.opcode & 0x000F == 0x0004:
                if self.v_register[(self.opcode & 0x00F0) >> 4] > \
                    (0xFF - self.v_register[(0x0F00) >> 8]):
                    self.v_register[0xF] = 1
                else:
                    self.v_register[0xF] = 0
                self.v_register[(self.opcode & 0x0F00) >> 8] += \
                    self.v_register[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
            elif self.opcode & 0x000F == 0x0005:
                if self.v_register[(self.opcode & 0x00F0) >> 4] > \
                    self.v_register[(self.opcode & 0x0F00) >> 8]:
                    self.v_register[0xF] = 0
                else:
                    self.v_register[0xF] = 1
                self.v_register[(self.opcode & 0x0F00) >> 8] -= \
                    self.v_register[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
            elif self.opcode & 0x000F == 0x0006:
                self.v_register[0xF] = self.v_register[(self.opcode & 0x0F00) >> 8] \
                    & 0x01
                self.v_register[(self.opcode & 0x0F00) >> 8] = \
                    self.v_register[(self.opcode & 0x0F00) >> 8] >> 1
                self.pc += 2
            elif self.opcode & 0x000F == 0x0007:
                if self.v_register[(self.opcode & 0x0F00) >> 8] > \
                    self.v_register[(self.opcode & 0x00F0) >> 4]:
                    self.v_register[0xF] = 0
                else:
                    self.v_register[0xF] = 1
                self.v_register[(self.opcode & 0x0F00) >> 8] = \
                    self.v_register[(self.opcode & 0x00F0) >> 4] - \
                    self.v_register[(self.opcode & 0x0F00) >> 8]
                self.pc += 2
            elif self.opcode & 0x000F == 0x000E:
                self.v_register[0xF] = self.v_register[(self.opcode & 0x0F00) >> 8] \
                    & 0x80 >> 7
                self.v_register[(self.opcode & 0x0F00) >> 8] = \
                    self.v_register[(self.opcode & 0x0F00) >> 8] << 1
                self.pc += 2
        
        elif tmp == 0x9000:
            if self.v_register[(self.opcode & 0x0F00) >> 8] != \
                self.v_register[(self.opcode & 0x00F0) >> 4]:
                self.pc += 4
            else:
                self.pc += 2
        elif tmp == 0xA000:
            self.I = self.opcode & 0x0FFF
            self.pc += 2
        elif tmp == 0xB000:
            self.pc = self.v_register[0x0] + self.opcode & 0x0FFF
        elif tmp == 0xC000:
            self.v_register[(self.opcode & 0x0F00) >> 8] = \
                random.randint(0, 255) & self.opcode & 0x00FF
            self.pc += 2
        elif tmp == 0xD000:
            x = self.v_register[(self.opcode & 0x0F00) >> 8]
            y = self.v_register[(self.opcode & 0x00F0) >> 4]
            height = self.opcode & 0x000F
            pixel = 0

            self.v_register[0xF] = 0
            for y_line in range(height):
                pixel = self.memory[self.I + y_line]
                for x_line in range(8):
                    if pixel & (0x80 >> x_line) != 0:
                        if self.gfx[(x + x_line + (y + y_line * 64))] == 1:
                            self.v_register[0xF] = 1
                        self.gfx[(x + x_line + (y + y_line) * 64)]  = \
                            self.gfx[(x + x_line + (y + y_line) * 64)] ^ 1

            self.draw_flag = True
            self.pc += 2
        elif tmp == 0xE000:
            if self.opcode & 0x000F == 0x000E:
                if self.key[self.v_register[(self.opcode & 0x0F00) >> 8]] != 0:
                    self.pc += 4
                else:
                    self.pc += 2
            elif self.opcode & 0x000F == 0x0001:
                if self.key[self.v_register[(self.opcode & 0x0F00) >> 8]] == 0:
                    self.pc += 4
                else:
                    self.pc += 2
        
        elif tmp == 0xF000:
            if self.opcode & 0x000F == 0x0007:
                self.v_register[(self.opcode & 0x0F00) >> 8] = \
                    self.d_timer
                self.pc += 2
            elif self.opcode & 0x000F == 0x000A:
                for key in range(16):
                    if self.key[key] != 0:
                        self.v_register[(self.opcode & 0x0F00) >> 8] = key
                self.pc += 2
            elif self.opcode & 0x000F == 0x0008:
                self.s_timer = self.v_register[(self.opcode & 0x0F00) >> 8]
                self.pc += 2
            elif self.opcode & 0x000F == 0x000E:
                if self.v_register[(self.opcode & 0x0F00) >> 8] > \
                    (0xFFF - self.I):
                    self.v_register[0xF] = 1
                else:
                    self.v_register[0xF] = 0
                self.I += self.v_register[(self.opcode & 0x0F00) >> 8]
                self.pc +=  2
            elif self.opcode & 0x000F == 0x0009:
                self.I = int(self.v_register[(self.opcode & \
                    0x0F00) >> 8] * 0x5)
                self.pc += 2
            elif self.opcode & 0x000F == 0x0003:
                self.memory[self.I] = self.v_register[(self.opcode & \
                    0x0F00) >> 8] / 100
                self.memory[self.I + 1] = (self.v_register[(self.opcode & \
                    0x0F00) >> 8] / 10) % 10
                self.memory[self.I + 2] = (self.v_register[(self.opcode & \
                    0x0F00) >> 8] % 10) % 10
                self.pc += 2
            elif self.opcode & 0x000F == 0x0005:
                if self.opcode & 0x00F0 == 0x0010:
                    self.d_timer = self.v_register[(self.opcode & 0x0F00) >> 8]
                    self.pc += 2
                elif self.opcode & 0x00F0 == 0x0050:
                    for val in range((self.opcode & 0x0F00) >> 8):
                        self.memory[self.I + val] = self.v_register[val]
                    self.pc += 2
                elif self.opcode & 0x00F0 == 0x0060:
                    for val in range((self.opcode & 0x0F00) >> 8):
                        self.v_register[val] = self.memory[self.I + val]
                    self.pc += 2

        
        else:
            print("Unknown opcode {0}").format(self.opcode)

        if self.d_timer > 0:
            self.d_timer -= 1

        if self.s_timer > 0:
            if self.s_timer == 1:
                sound.play()
            self.s_timer -= 1