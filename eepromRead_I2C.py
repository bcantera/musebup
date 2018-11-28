#!/usr/bin/env python

import serial
import time
import binascii

#Function for printing offsets
def printOffsets():
   out = ''
   while ser.inWaiting() > 0:
      out += ser.read(1)
   if out != '':
      out = out.split("\n",7)[7];
      out = out.split("I2C STOP BIT",1)[0];
      out = out.replace("READ: 0x", "")
      out = out.replace("  ACK 0x","")
      out = out.replace("ACK", "")
      out = out.replace("NACK", "")
      out = out.replace("\n","")
      print out + '\n'
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

#Search for available memory addresses
ser.write('(1)\n')
time.sleep(0.5)
out = ''
while ser.inWaiting() > 0:
   out += ser.read(1)
   out = out.replace("\n", "")
   out = out.replace("(1)", "")
   out = out.replace("Searching I2C address space. Found devices at:", "")
   out = out.replace("I2C>", "")

#If any address is found, print it
if '0x' in out:
   print 'Found addresses:\n' + out + '\n'
   offsetsW = out.split(") ")
   offsetsR = out.split(") ")

   #Build W addresses array
   y = offsetsW.index(max(offsetsW))
   while y != -3:
      offsetsW[y+1] = offsetsW[y+1][:-7]
      del offsetsW[y]
      y = y - 2

   #Build R addresses array
   y = offsetsR.index(max(offsetsR))
   while y != -3:
      del offsetsR[y+1]
      y = y - 2

   y = offsetsR.index(max(offsetsR))
   while y != -1:
      offsetsR[y] = offsetsR[y][:-7]
      y = y -1

   #Read and print offsets
   y = offsetsR.index(min(offsetsR))
   for y in range(0, offsetsR.index(max(offsetsR))+1):
      readOffset = '[' + offsetsW[y] + ' 0x00][' + offsetsR[y] + ' r:1024]\n'
      ser.write(readOffset)
      time.sleep(0.5)
      print offsetsR[y] + ':'
      printOffsets()

else:
    print 'No addresses found'

ser.close()
