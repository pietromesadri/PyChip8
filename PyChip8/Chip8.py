class chip8:
    def __init__(self, renderer, stack, 
                 v_register, memory, chip8_fontset,
                 d_timer, s_timer):
        self.pc = 0x200
        self.opcode = 0
        self.I = 0
        self.sp = 0
        self.renderer = renderer
        self.stack = stack
        self.v_register = v_register
        self.memory = memory
        self.fontset = chip8_fontset
        self.d_timer = d_timer
        self.s_timer = s_timer

        self.renderer.clear_screen()
        self.stack = 0
        self.v_register = []
        self.memory = []

        for i in range(80):
            self.memory[i] = self.fontset[i]

        self.s_timer = ""
        self.d_timer = ""

    def load_game(self, game):
        with open(game, "rb") as g:
            for b in g.read():
                self.memory.append(b)
        return 1

    def  emulate_cycle(self):
        # Fetch opcode
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]

        # Decode opcode
        tmp = self.opcode & 0xF000
        if tmp == 0x0000:
            if self.opcode & 0x000F == 0x0000:
                self.renderer.clear_screen()
            elif self.opcode & 0x000F == 0x000E:
                return
        elif tmp == 0x1000:
            self.pc = self.opcode & 0x0FFF
        elif tmp == 0x2000:
            self.stack[self.sp] = self.pc
            self.sp += 1
            self.pc = self.opcode & 0x0FFF
        elif tmp == 0x3000:
            if self.v_register[(self.opcode & 0x0F00) >> 8] == (self.opcode & 0x00FF):
                self.pc += 2
        elif tmp == 0x4000:
            if self.v_register[(self.opcode & 0x0F00) >> 8] != (self.opcode & 0x00FF):
                self.pc += 2
        elif tmp == 0x5000:
            if self.v_register[(self.opcode & 0x0F00) >> 8] == self.v_register[(self.opcode & 0x00F0) >> 4]:
                self.pc += 2
        elif tmp == 0x6000:
            self.v_register[(self.opcode & 0x0F00) >> 8] = self.opcode & 0x00FF
        elif tmp == 0x7000:
            self.v_register[(self.opcode & 0x0F00) >> 8] += self.opcode & 0x00FF
        elif tmp == 0x8000:
            self.v_register[(self.opcode & 0x0F00) >> 8] = self.v_register[(self.opcode & 0x00F0) >> 4]
        else:
            print("Unknown opcode {0}").format(self.opcode)

        if self.d_timer > 0:
            self.d_timer -= 1

        if self.s_timer > 0:
            if self.s_timer == 1:
                print("beep")
            self.s_timer -= 1