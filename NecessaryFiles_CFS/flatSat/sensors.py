#---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------
# Project: CFS+Cosmos
# Author: Rebeca Rodrigues
# Date: 07/2016
# Contact: rebeca.n.rod@gmail.com
# Function: This piece of software is responsible for receive commands from the cFS Telemetry
# Sistem Tool(EventMessage.py) and respond 'appropriated', interface with sensors, and send
# data packets back to a control center - Cosmos
# Adapted from: Guilherme Korol (07/2015)

# Please, feel free to finish implementing the things that are not done yet ;)
# Execute it on Python3
#---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------

import time
import microstacknode.hardware.accelerometer.mma8452q
import spidev
import os
import datetime
import socket
import shlex
import subprocess
from multiprocessing.connection import Listener
from array import array

#defines
light_channel = 0
temp_channel  = 1
id = 999
global frame_count, command_count
frame_count = 0
command_count = 0

CMDUTIL_path = '../cmdUtil/cmdUtil'
HOST = 'XX.X.XXX.XXX'     #destination address
PORT = '5005'		  #just a port (where Cosmos is listening)
PKTID = '0x1808'	  #packet id (required by cmdUtil) will be useful later on
ENDIAN = 'BE'		  #endianess (matching with Cosmos target config)
CMDCODE = '6'		  #command code (required by cmdUtil) will be useful later on

#initializating SPI (ADC)
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

#initializating I2C (accelerometer)   --not fully implemented yet 
#Comment out the next 2 lines if not intyend to use an accelerometer
accelerometer = microstacknode.hardware.accelerometer.mma8452q.MMA8452Q()
accelerometer.open()

fileEnable = True		#creates a local log file

#function: read light value, print on terminal, and save on log file if enabled
#no parameters, ADC channel set as constant 'light_channel'
#returns value (0 - 1023)
def light():			
        light_level = ReadChannel(light_channel)
        light_volts = ConvertVolts(light_level,2)
        print(("Light : {} ({}V)".format(light_level,light_volts)))
        if(fileEnable):
                log = open("log.txt","a")
                time = datetime.datetime.now()
                log.write("\n" + str(time))
                log.write(("\nLGT - Light : {} ({}V)\n".format(light_level,light_volts)))
                log.close()
        return light_level

#function: read temperature value, print on terminal, and save on log file if enabled
#no parameters, ADC channel set as constant 'temp_channel'
#returns value (0 - 1023)
def temp():
        temp_level = ReadChannel(temp_channel)
        temp_volts = ConvertVolts(temp_level,2)
        temp       = ConvertTemp(temp_level,2)
        print(("Temp  : {} ({}V) {} deg C".format(temp_level,temp_volts,temp)))
        if(fileEnable):
                log = open("log.txt","a")
                time = datetime.datetime.now()
                log.write("\n" + str(time))
                log.write(("\nTMP - Temp  : {} ({}V) {} deg C\n".format(temp_level,temp_volts,temp)))
                log.close()
        return temp_level

#function: read accelerometer values, print on terminal, and save on log file if enabled
#no parameters
#no return
def accel():
	#comment the next lines if no acc sensor is connected
        #x, y, z = accelerometer.get_xyz()
	print('Accel:')
        #print('x: {}, y: {}, z: {}'.format(x, y, z))
        #if(fileEnable):
        #        log = open("log.txt","a")
        #        time = datetime.datetime.now()
        #        log.write("\n" + str(time))
        #        log.write("\nACC - x: {}, y: {}, z: {}\n".format(x, y, z))
        #        log.close()

#function: call all sensor readings and telemetry sender
#no parameters
#no return
def all():
        lgtTlm = light()
        tmpTlm = temp()
        accel()
        sendTlm(lgtTlm, tmpTlm)

#function: call all sensor readings and telemetry sender
#no parameters
#no return
def sendTlm(val1, val2):
        global frame_count, command_count
        frame_count +=1
        launch_string = (CMDUTIL_path + ' --host=' + HOST + ' --port=' + PORT + ' --pktid=' + PKTID
                         + ' --endian=' + ENDIAN + ' --cmdcode=' + CMDCODE
                         + ' --long=' + str(frame_count)
                         + ' --long=' + str(time.time())
                         + ' --string=' + '8:' + str(val2).zfill(4) + str(val1).zfill(4)
                         + ' --long=' + str(command_count)
                         )
        cmd_args = shlex.split(launch_string)
        subprocess.Popen(cmd_args)
        
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
#from http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/
def ReadChannel(channel):
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places. 
#from http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/
def ConvertVolts(data,places):
	volts = (data * 3.3) / float(1023)
	volts = round(volts,places)  
	return volts
  
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
#from http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/
def ConvertTemp(data,places):

  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  388       75    1.25
  #  465      100    1.50
  #  543      125    1.75
  #  620      150    2.00
  #  698      175    2.25
  #  775      200    2.50
  #  853      225    2.75
  #  930      250    3.00
  # 1008      275    3.25
  # 1023      280    3.30

	temp = ((data * 330)/float(1023))-50
	temp = round(temp,places)
	return temp

#prepare communication with tlmUtil (port 6000)
address = ('localhost', 6000)
listener = Listener(address)
conn = listener.accept()

#main loop, keep looking for new commands
while(True):
	try:
                msg = conn.recv()
	except EOFError:
		print("EOFError, is EventMessages.py running?")
		pass
	
        #PRINT LIGHT COMMAND
	if msg == "LGT":
		command_count += 1
		light()
	#PRINT TEMPERATURE COMMAND
	elif msg == "TMP":
        	command_count += 1
        	temp()
	#PRINT ACCELEROMETER COMMAND
	elif msg == "ACC":
        	command_count += 1
        	accel()
	#PRINT LIGHT, TEMP, AND ACCELEROMETER
	elif msg == "ALL":
                command_count += 1
                all()                           
	elif msg == "SID":
                command_count += 1
                print('SAT ID: {}'.format(id))
        #MONITORING COMMAND - KEEP SENDING TELEMETRY(AND PRINTING ON SCREEN) TO COSMOS 
	elif msg == "MNT":
	#	frame_count = 0
		command_count += 1
		while msg != 'STP':
			all()
			time.sleep(1.5)
			try:
				#conn = listener.accept()
				#msg = conn.recv()
                                if (conn.poll()):
                                        msg = conn.recv()
			except EOFError:
                                print("\nWaiting command to stop\n")
		command_count +=1 
		print("Stopping telemetry...")
	#DISABLE FILE COMMAND - REPLICATES
	elif msg == "STP":
		command_count += 1
		#DO SOMETHING, I DONT KONW YET WHAT
		print("\nSTOP TLM\n")
        #DISABLE LOCAL LOG FILE
	elif msg == "DFL":
                command_count += 1
                fileEnable = False
                print("\nLOG FILE DISABLE\n")
        #IDLE
	elif msg == "IDL":
		command_count += 1
		pass                        
	else:
                print("Usage: XXX")
                print("Commands:TMP - TEMPERATURE, \n\t LGT - LIGHT,\n\t ACC - ACCELEROMETER,\n\t SID - SAT ID,\n\t ALL - ALL SENSORS,\n\t MNT - MONITORING ON,\n\t DFL - DISABLE LOG FILE")
	msg = "IDL"           #default

listner.close()
