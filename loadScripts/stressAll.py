#!/bin/python


import subprocess
import time
import sys

args = sys.argv

#VCPU, IO,Memory, Disk, Utilization
if not len(args)== 7:
        print("Incorrect number of arguments")
        exit()

#get arguments
vcpu = args[1]
io = args[2]
mem = args[3]
disk = args[4]
util = args[5]
timeout = args[6]


for i in range(len(args)):
        if not i==0 and not (args[i].isnumeric() and  int(args[i])>= 0):
                print("Wrong Input Argument")
                exit()


timeout = int(timeout)
u = int(util)
print('Duration:',timeout)


#Start load with stress

for j in range(timeout):
      print("Minutes:",j)
      t = int((u/100)*60)
      p = subprocess.Popen(['stress','--cpu',str(vcpu),'--io',str(io),'--vm',str(mem),'--hdd',str(disk),'--timeout',str(t)], stdout=subprocess.PIPE,universal_newlines=True)
      time.sleep(60)
