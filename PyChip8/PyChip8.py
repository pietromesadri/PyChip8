from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame, Render, Input

opcode = 0
index_register = 0
program_counter = 0
stack_pointer = 0
memory = []
registers_V = []
gfx = []
stack = []
key = []
delay_timer = ""
sound_timer = ""

def main():
    renderer = Render.Renderer(640,320)
    input = Input.Input()

    running = 1

    renderer.clear_screen(255,255,0)
    
    while running:
        running = input.event_handler()

main()