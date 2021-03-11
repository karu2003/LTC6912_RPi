#! /usr/bin/python
"""
example of controlling the amplifier LTC6912-2 on Raspberry Pi.
CLI control  
"""

import sys
import curses
import gpiozero

GAIN_dB  = ['-120', '0', '6','12','18.1','24.1','30.1','36.1','-12x']
GAIN_HEX = [  0x00,0x11,0x22,0x33,  0x44,  0x55,  0x66,  0x77,  0x88]
PreAmp_On = gpiozero.LED(12)
Gain_Low  = gpiozero.LED(16)

def main(stdscr):
    LTC69122 = gpiozero.SPIDevice(port=0, device=0)
    x = 0
    stdscr.nodelay(1)
    stdscr.addstr('arrow up and down for GAIN control')
    stdscr.move(1, 0)
    stdscr.addstr('Gain dB = '+ str(GAIN_dB[x]) + '     ')
    LTC69122._spi.transfer([GAIN_HEX[x]])
    stdscr.refresh()
    stdscr.move(1, 0)
    PreAmp_On.on()
    Gain_Low.off()
    while True:
        # get keyboard input, returns -1 if none available
        c = stdscr.getch()
        if c != -1:
            if c == 259: # 258 - down, 259 - up, 260 - <, 261 - >
                if x <= 7:
                    x += 1
            else:
                if x >= 1:
                    x -= 1
            stdscr.addstr('Gain dB = '+ str(GAIN_dB[x]) + '     '  )
            stdscr.refresh()
            # return curser to start position
            stdscr.move(1, 0)
            LTC69122._spi.transfer([GAIN_HEX[x]])

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        PreAmp_On.off()
        Gain_Low.off()
        sys.exit('\nInterrupted by user') 
    