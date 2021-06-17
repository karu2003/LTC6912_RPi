#! /usr/bin/python
"""
example of controlling the amplifier LTC6912-2 on Raspberry Pi.
CLI control  
"""

import sys
import curses
import gpiozero
from SC18IS602B import SC18IS602B
from MCP230XX import MCP230XX
from LTC1380 import LTC1380

GAIN_dB  = ['-120', '0', '6','12','18.1','24.1','30.1','36.1','-12x']
GAIN_HEX = [  0x00,0x11,0x22,0x33,  0x44,  0x55,  0x66,  0x77,  0x88]

MCP = MCP230XX('MCP23008', i2cAddress=0x20)
MUX = LTC1380(i2cAddress=0x48)

USBL_On = 1
PreAmp_On = 2
Gain_Low  = 3
RX_LIM  = 5
RX_MAIN  = 6
ON = 1
OFF = 0


def main(stdscr):
    MCP.set_mode(USBL_On, 'output')
    MCP.set_mode(PreAmp_On, 'output')
    MCP.set_mode(Gain_Low, 'output')
    MUX.SetChannel(RX_MAIN)
    LTC69122 = SC18IS602B(i2cAddress=0x28, speed="CLK_1843_kHz", mode="MODE_0", order="MSB")
    x = 0
    stdscr.nodelay(1)
    stdscr.addstr('arrow up and down for GAIN control')
    stdscr.move(1, 0)
    stdscr.addstr('Gain dB = '+ str(GAIN_dB[x]) + '     ')
    # LTC69122._spi.transfer([GAIN_HEX[x]])
    LTC69122.spiTransfer(slaveNum=0, txData=[GAIN_HEX[x]], rxLen=len([GAIN_HEX[x]]))
    stdscr.refresh()
    stdscr.move(1, 0)
    MCP.output(USBL_On, OFF)
    MCP.output(PreAmp_On, ON)
    MCP.output(Gain_Low, OFF)
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
            # LTC69122._spi.transfer([GAIN_HEX[x]])
            LTC69122.spiTransfer(slaveNum=0, txData=[GAIN_HEX[x]], rxLen=len([GAIN_HEX[x]]))

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        MCP.output(PreAmp_On, OFF)
        MCP.output(Gain_Low, OFF)
        sys.exit('\nInterrupted by user') 
    