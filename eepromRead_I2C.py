#!/usr/bin/env python

import serial
import time
import binascii
import io

def printOffsets ( str ):
    
   out = ''
   while ser.inWaiting() > 0:
      out += ser.read(1)
   if out != '':
      out = out.split("\n",7)[7];
      out = out.split("I2C STOP BIT",1)[0];
      out = out.replace("READ: 0x", "")
      out = out.replace("  ACK 0x","")
      out = out.replace("NACK", "")
      out = out.replace("\n","")
      print out
   time.sleep(0.5)
   ser.reset_input_buffer()
   ser.reset_output_buffer()
   
   return;

#Open Bus Pirate serial connection and clear previous input/output buffers
ser = serial.Serial('/dev/ttyACM0', baudrate=115200, bytesize=8, parity='N', stopbits=1)
ser.reset_input_buffer()
ser.reset_output_buffer()

#Read current mode
ser.write('\n')
mode = ser.read(6)
mode = mode.replace('\n','')
mode = mode.replace(' ','')

#Setup Bus Pirate for I2C
if mode.encode("hex") != '0d4932433e':
   ser.write('\n')
   ser.write('\n')
   ser.write('\n')
   ser.write('m4\n')
   ser.write('2\n')
   ser.write('2\n')
   ser.write('W\n')
   ser.write('P\n')
   time.sleep(0.5)
   ser.reset_input_buffer()
   ser.reset_output_buffer()

output = ''

#Read 0xa1
ser.write('[0xa0 0x00][0xa1 r:256]\n')
time.sleep(0.5)
print '0xa1:'
printOffsets(output)

#Read 0xa3
ser.write('[0xa2 0x00][0xa3 r:256]\n')
time.sleep(0.5)
print '0xa3:'
printOffsets(output)

#Read 0xa5
ser.write('[0xa4 0x00][0xa5 r:256]\n')
time.sleep(0.5)
print '0xa5:'
printOffsets(output)

#Read 0xa7
ser.write('[0xa6 0x00][0xa7 r:256]\n')
time.sleep(0.5)
print '0xa7:'
printOffsets(output)

ser.close()
