#!/bin/python
import threading
import subprocess
import time
import sys
import datetime
args = sys.argv

    
def main():

    if not len(args)== 8:
            print("Incorrect number of arguments")
            exit()

    #get arguments
    ##interval and duration in minutes
    vcpu = args[1]
    io = args[2]
    mem =args[3]
    disk =args[4]
    interval = args[5]
    timeout = args[6]
    trace_ID = args[7]


    for i in range(len(args)):
            if not i==0 and not (args[i].isnumeric() and  int(args[i])>= 0):
                    print("Wrong Input Argument")
                    exit()

    #Load Trace File
    print('Loading VM Trace')
    utils = []
    traceDataset_path = "azureTrace/azure/"
    f = open(traceDataset_path+str(trace_ID), "r")

    #Get CPU Usage timeseries 
    for u in f:
            u = u.strip()
            if u.isnumeric() and int(u)>= 0:
                utils.append(int(u))


    print("Trace Size:"+ str(len(utils)))

    interval = int(interval)
    max_iter = int(int(timeout)/interval)

    #Start data recording
    print("Max_Iterations: "+str(max_iter))
    thread1 = threading.Thread(target=recordInfo, args=(int(timeout),))
    thread1.start()


    #Start Simulating load with Stress-ng
    for i in range(max_iter):
            u = utils[i]
            print('Interval Average CPU Usage:',str(u))
            #Each Minute of the interval
            #e.g., if Usage is 50% for 5 minute, genrate load for 50% of each minute during the 5 minute interval and sleep: (30sec * 5) actice, (30sec * 5) sleep.   
            for j in range(interval):
                    print("Minute:",j)
                    t = int((u/100)*60)
                    #parallel process
                    p = subprocess.Popen(['stress','--cpu',str(vcpu),'--io',str(io),'--vm',str(mem),'--hdd',str(disk),'--timeout',str(t)], stdout=subprocess.PIPE,universal_newlines=True)
                    time.sleep(60)
            #log information
            with open("log_file.csv", 'a') as f:
                    f.write(str(datetime.datetime.now())+','+str(u)+','+str(vcpu)+'\n')

            print("interval:"+ str(i)+' '+str(datetime.datetime.now()))

            if i >= len(utils):
                    i=0
    thread1.join()

def recordInfo(timeout):
    startTime = time.time()
    # OS statistics to record
    stat = ['r','b','swpd','free','buff','cache','si','so','bi','bo','in','cs','us','sy','id','wa','st']
    with open("log_usage.csv", 'a') as f:
        f.write('TimeStamp,'+','.join(stat)+'\n')
    
    while time.time() - startTime < timeout:

        p = subprocess.Popen(['vmstat','1','2'],stdout=subprocess.PIPE,universal_newlines=True)
        output = ''
        try:
            stdout, stderr = p.communicate(timeout=2*60)
            output = stdout
        except Exception as e:
            print(e)
            return None
	
        if output == '' or len(output)==0:
            print('Cannot get VM Info')
            break
        
        output = output.split('\n')
        line = output[3].split()
        info = []
        for i in range(len(stat)):
            info.append(str(line[i]))

        with open("log_usage.csv", 'a') as f:
            f.write(str(datetime.datetime.now())+','+','.join(info)+'\n')

if __name__ == "__main__":
    main()



