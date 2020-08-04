#!/usr/bin/env python

import os
import time
import serial

#Check for execution privileges
def privCheck():
    if os.getuid() != 0:
       print ("###Root privileges required, please run either as root or with sudo")
       isAllowed = False
    else:
       isAllowed = True
    return isAllowed

#Check for previous dump.hex
def dumpCheck():

    if os.path.isfile('dump.hex') == True:
        checking = True
        while checking:
            confirm_delete = input("File dump.hex found, delete it? (y/n)\n")
            if confirm_delete == "y":
                os.remove("dump.hex")
                checking = False
            elif confirm_delete == "n":
                print ("Appending to actual dump.hex")
                checking = False
            else:
                print ("\n### Incorrect option, please type \"y\" or \"n\" \n")

#Menu design
def menu():
   menu = True
   while menu and privCheck:
       print (31 * "-" , "MENU" , 31 * "-")
       print ("1. Dump EEPROM")
       print ("2. Write EEPROM")
       print ("3. Exit")
       print (68 * "-")

       option = input()
       if option == '1':
          menu = False
       elif option == '2':
          menu = False
       elif option == '3':
          print ("###Quiting")
          menu = False
       else:
          print ("\n### Incorrect option, please select a valid option from the menu\n")
   return option

#Function for printing offsets
def printOffsets():
   out = ''
   palabra = ''
   while ser.inWaiting() > 0:
     out += ser.read(1).decode()
   if out != '':
     out = out.split("\n",7)[7];
     out = out.split("I2C STOP BIT",1)[0];
     out = out.replace("READ: 0x", "")
     out = out.replace("  ACK 0x"," ")
     out = out.replace("ACK", "")
     out = out.replace("NACK", "")
     out = out.replace("\n","")
     print (out + '\n')

     #Saving output to file
     f = open( 'dump.hex', 'a' )
     f.write( '\n' + out + '\n' )
     f.close()

   time.sleep(0.5)
   ser.reset_input_buffer()
   ser.reset_output_buffer()

   return;

checkPermission = privCheck()
checkBusPirate = os.path.exists('/dev/ttyACM0')
checkDump = dumpCheck()

if checkBusPirate == False and checkPermission :
   print ('### Bus pirate not found')

elif checkBusPirate and checkPermission and menu() == '1':

   #Open Bus Pirate serial connection and clear previous input/output buffers
   ser = serial.Serial('/dev/ttyACM0', baudrate=115200, bytesize=8, parity='N', stopbits=1)
   ser.reset_input_buffer()
   ser.reset_output_buffer()

   #Read current mode
   ser.write(b'\n')
   mode = str(ser.read(6))
   mode = mode.replace('\'','')
   mode = mode.replace('b\\r\\n','')

   #Setup Bus Pirate for I2C
   if mode != 'I2C>':
      ser.write(b'\n')
      ser.write(b'\n')
      ser.write(b'\n')
      ser.write(b'm4\n')
      ser.write(b'2\n')
      ser.write(b'2\n')
      ser.write(b'W\n')
      ser.write(b'P\n')
      time.sleep(0.5)
      ser.reset_input_buffer()
      ser.reset_output_buffer()

   #Search for available memory addresses
   ser.write(b'(1)\n')
   time.sleep(0.5)
   out = ''

   # Read (1) from buffer
   out = (ser.readline()).decode()

   # Read "Searching I2C address space. Found devices at:" from buffer
   out = (ser.readline()).decode()

   # Read actual addresses
   out = (ser.readline()).decode()

   if "Warning: *Short or no pull-up" in out:
      print ("\n### Message from Bus pirate:\n" + out + "\n")

   #If any address is found, print it
   if '0x' in out:
      print ('### Found addresses: \n' + out + '\n')
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
        ser.write(readOffset.encode())
        time.sleep(0.5)
        print (offsetsR[y] + ':')
        printOffsets()

   else:
      print ('### No addresses found')

   ser.close()
