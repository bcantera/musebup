#!/usr/bin/env python

import serial

#Open Bus Pirate serial connection
ser = serial.Serial('/dev/ttyACM0')

#Setup Bus Pirate for i2c
ser.write('\n')
ser.write('\n')
ser.write('m4\n')
ser.write('2\n')
ser.write('2\n')
ser.write('W\n')
ser.write('P\n')

line = ser.read(100)
print line

ser.close()
