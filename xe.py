from sys import argv,exit
from math import sqrt,sin,cos
from time import sleep
from msvcrt import getwch
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "true"
import pygame
from pygame import gfxdraw

if len(argv) == 1:
    print("Invalid usage.")
    exit(1)

with open(argv[1],'rb') as file:
    program = file.read()

def next():
    global idx
    idx += 1
    if idx < len(program):
        return program[idx]
    else:
        return None

def interrupt(type_,reg):
    # Console Operations
    # COUT R1
    if type_ == 0x11:
        print(chr(regs[reg]),end='')
    # CHIN R1
    elif type_ == 0x12:
        regs[reg] = ord(getwch())
    
    # Mathematical Operations
    # SQRT R1
    elif type_ == 0x21:
        regs[reg] = int(sqrt(regs[reg]))
    # SINE R1
    elif type_ == 0x22:
        regs[reg] = int(sin(regs[reg]))
    # COSS R1
    elif type_ == 0x23:
        regs[reg] = int(cos(regs[reg]))
    
    # Time Operations
    # WAIT R1
    elif type_ == 0x31:
        sleep(regs[reg])
    
    # Graphical Operations
    # OPNW R1
    elif type_ == 0x41:
        global window
        if not window:
            global display
            global clock
            global fps
            pygame.init()
            display = pygame.display.set_mode((500,500))
            clock = pygame.time.Clock()
            fps = regs[reg]
            window = True
            pygame.display.set_caption("Application")
        else:
            raise Exception("Already initialized window")
    # FLIP R1
    elif type_ == 0x42:
        if window:
            pygame.display.flip()
        else:
            raise Exception("Tried to flip frame buffer without opening a window first")
    # BLNK R1
    elif type_ == 0x43:
        if window:
            display.fill((0,0,0))
        else:
            raise Exception("Tried to clear frame buffer without opening a window first")
    # PIXL R1
    elif type_ == 0x44:
        if window:
            gfxdraw.pixel(display,regs[reg]+regs[reg+1],regs[reg+2]+regs[reg+3],(255,255,255))
        else:
            raise Exception("Tried to write to frame buffer without opening a window first")
    # LINE R1
    elif type_ == 0x45:
        if window == 0x45:
            gfxdraw.line(display,regs[reg]+regs[reg+1],regs[reg+2]+regs[reg+3],regs[reg+4]+regs[reg+5],regs[reg+6]+regs[reg+7],(255,255,255))
        else:
            raise Exception("Tried to write to frame buffer without opening a window first")
    # CIRC R1
    elif type_ == 0x46:
        if window:
            gfxdraw.circle(display,regs[reg]+regs[reg+1],regs[reg+2]+regs[reg+3],regs[reg+4]+regs[reg+5],(255,255,255))
        else:
            raise Exception("Tried to write to frame buffer without opening a window first")

idx = -1
opcode = next()
regs = [0] * 256
stack = []
sp = 0
window = False
clock = None
display = None
fps = 60
running = True
op = None

while opcode and running:
    # NOP
    if opcode == 0x00:
        op = "NOP"
        next()
        next()
    # MOV R1,D1
    elif opcode == 0x01:
        r1 = next()
        d1 = next()
        op = f'MOV {hex(r1)},{hex(d1)}'
        regs[r1] = d1
    # MOV R1,R2
    elif opcode == 0x02:
        r1 = next()
        r2 = next()
        op = f'MOV {hex(r1)},{hex(r2)}'
        regs[r1] = regs[r2]
    # ADD R1,D1
    elif opcode == 0x03:
        r1 = next()
        d1 = next()
        op = f'ADD {hex(r1)},{hex(d1)}'
        regs[r1] += d1
    # ADD R1,R2
    elif opcode == 0x04:
        r1 = next()
        r2 = next()
        op = f'ADD {hex(r1)},{hex(r2)}'
        regs[r1] += regs[r2]
    # SUB R1,D1
    elif opcode == 0x05:
        r1 = next()
        d1 = next()
        op = f'SUB {hex(r1)},{hex(d1)}'
        regs[r1] -= d1
    # SUB R1,R2
    elif opcode == 0x06:
        r1 = next()
        r2 = next()
        op = f'SUB {hex(r1)},{hex(r2)}'
        regs[r1] -= regs[r2]
    # MUL R1,D1
    elif opcode == 0x07:
        r1 = next()
        d1 = next()
        op = f'MUL {hex(r1)},{hex(d1)}'
        regs[r1] *= d1
    # MUL R1,R2
    elif opcode == 0x08:
        r1 = next()
        r2 = next()
        op = f'MUL {hex(r1)},{hex(r2)}'
        regs[r1] *= regs[r2]
    # DIV R1,D1
    elif opcode == 0x09:
        r1 = next()
        d1 = next()
        op = f'DIV {hex(r1)},{hex(d1)}'
        regs[r1] /= d1
    # DIV R1,R2
    elif opcode == 0x0A:
        r1 = next()
        r2 = next()
        op = f'DIV {hex(r1)},{hex(r2)}'
        regs[r1] /= regs[r2]
    # JMP A1
    elif opcode == 0x0B:
        a1 = next()
        next()
        op = f'JMP {hex(a1)}'
        idx = a1-1
    # CALL A1
    elif opcode == 0x0C:
        a1 = next()
        next()
        op = f'CALL {hex(a1)}'
        stack.append(idx)
        idx = a1-1
        sp += 1
    # RET
    elif opcode == 0x0D:
        next()
        next()
        op = "RET"
        sp -= 1
        idx = stack[sp]
        stack.remove(stack[sp])
    # INC R1
    elif opcode == 0x0E:
        r1 = next()
        next()
        op = f'INC {hex(r1)}'
        regs[r1] += 1
    # DEC R1
    elif opcode == 0x0F:
        r1 = next()
        next()
        op = f"DEC {hex(r1)}"
        regs[r1] -= 1
    # AND R1,R2
    elif opcode == 0x10:
        r1 = next()
        r2 = next()
        op = f'AND {hex(r1)},{hex(r2)}'
        regs[r1] = regs[r1] & regs[r2]
    # OR R1,R2
    elif opcode == 0x11:
        r1 = next()
        r2 = next()
        op = f'OR {hex(r1)},{hex(r2)}'
        regs[r1] = regs[r1] | regs[r2]
    # XOR R1,R2
    elif opcode == 0x12:
        r1 = next()
        r2 = next()
        op = f'XOR {hex(r1)},{hex(r2)}'
        regs[r1] = regs[r1] ^ regs[r2]
    # HALT
    elif opcode == 0x13:
        next()
        next()
        op = "HALT"
        running = False
    # INT D1,R1
    elif opcode == 0x14:
        d1 = next()
        r1 = next()
        op = f'INT {hex(d1)},{hex(r1)}'
        interrupt(d1,r1)
    # JE R1,R2
    elif opcode == 0x15:
        r1 = next()
        r2 = next()
        op = f'JE {hex(r1)},{hex(r2)}'
        if r1 == r2:
            next()
            next()
            next()
    # JNE R1,R2
    elif opcode == 0x16:
        r1 = next()
        r2 = next()
        op = f'JNE {hex(r1)},{hex(r2)}'
        if r1 != r2:
            next()
            next()
            next()
    # JGT R1,R2
    elif opcode == 0x17:
        r1 = next()
        r2 = next()
        op = f'JGT {hex(r1)},{hex(r2)}'
        if r1 > r2:
            next()
            next()
            next()
    # JLT R1,R2
    elif opcode == 0x18:
        r1 = next()
        r2 = next()
        op = f'JLT {hex(r1)},{hex(r2)}'
        if r1 < r2:
            next()
            next()
            next()
    # JGTE R1,R2
    elif opcode == 0x19:
        r1 = next()
        r2 = next()
        op = f'JGTE {hex(r1)},{hex(r2)}'
        if r1 >= r2:
            next()
            next()
            next()
    # JLTE R1,R2
    elif opcode == 0x20:
        r1 = next()
        r2 = next()
        op = f'JLTE {hex(r1)},{hex(r2)}'
        if r1 <= r2:
            next()
            next()
            next()
    
    if window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if running:
            clock.tick(fps)
    
    opcode = next()

pygame.quit()
exit(0)