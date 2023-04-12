import psutil
import time
import time
import sys

#takes percentage memeory usage (1-100) & duration of emulation in seconds
def memory_simulation(mem,duration):

	total_memory = psutil.virtual_memory().total

	required_memory = int(total_memory * (mem/100))
	memory = [0] * (required_memory // 8)
	print("Allocated--")
	start = time.time()	
	while True:
		current = time.time()
		if (current-start) >= duration:
			break
	available_memory = psutil.virtual_memory().available
	print("Percentage Memory Usage",((total_memory - available_memory)/total_memory)*100)
	print("END")


def main():

	args = sys.argv

	#VCPU, IO,Memory, Disk, Utilization
	if not len(args)== 3:
		print("Incorrect number of arguments")
		exit()

	#get arguments
	util = args[5]
	timeout = args[6]


	for i in range(len(args)):
			if not i==0 and not (args[i].isnumeric() and  int(args[i])>= 0):
				print("Wrong Input Argument")
				exit()


	timeout = int(timeout)
	u = int(util)
	print('Duration:',timeout)
	memory_simulation(util,timeout)


if __name__ == '__main__':

	main()

