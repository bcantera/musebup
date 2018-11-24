#!/usr/bin/env python

import serial

#Open Bus Pirate serial connection
ser = serial.Serial('/dev/ttyACM0')

#Read current mode
ser.write('\n')
mode = ser.read(5)

#Setup Bus Pirate for i2c
if mode != 'I2C':
   ser.write('\n')
   ser.write('\n')
   ser.write('m4\n')
   ser.write('2\n')
   ser.write('2\n')
   ser.write('W\n')
   ser.write('P\n')

#Read address and print it (redirect to file with "command >> output.log)"
ser.write('[0xa1 r:256]\n')
line = ser.readline()
print line

ser.close()
