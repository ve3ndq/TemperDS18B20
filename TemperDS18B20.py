#! /usr/bin/python2.7

import os                                                  # import os module
import glob                                                # import glob module
import time                                                # import time module
import datetime

import mysql.connector
import time
stime = time.strftime('%Y-%m-%d %H:%M:%S')


mydb = mysql.connector.connect(
  host="localhost",
  user="pi",
  passwd="raspberry",
  database="temper"
)

mycursor = mydb.cursor()

os.system('modprobe w1-gpio')                              # load one wire communication device kernel modules
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'                          # point to the address
device_folder = glob.glob(base_dir + '28*')[0]             # find device with address starting from 28*
device_file = device_folder + '/w1_slave'                  # store the details
f1=open('/var/www/html/out.html','a')
strC=""
strF=""
strTime=""



def read_temp_raw():
   f = open(device_file, 'r')
   lines = f.readlines()                                   # read the device details
   f.close()
   return lines

def read_temp():
   lines = read_temp_raw()
   while lines[0].strip()[-3:] != 'YES':                   # ignore first line
      time.sleep(0.2)
      lines = read_temp_raw()
   equals_pos = lines[1].find('t=')                        # find temperature in the details
   if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string) / 1000.0                 # convert to Celsius
      temp_f = temp_c * 9.0 / 5.0 + 32.0                   # convert to Fahrenheit
      strC=str(temp_c)
      f1.write(str(temp_c)+','+ datetime.datetime.now().isoformat()+'\n')
      sql = "INSERT INTO temper (temp,location) VALUES (%s,%s);"
      val = (temp_c,'basement')
      print (sql,val)
      mycursor.execute(sql,val)
      mydb.commit()
      #return temp_c, temp_f, time.asctime( time.localtime(time.time()) )
      return strC
while True:
   #print(read_temp(),file=f1)                                      # Print temperature
   #read_temp()
   print(read_temp()+time.asctime( time.localtime(time.time())))
   time.sleep(10)
