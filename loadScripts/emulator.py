
import time
import subprocess


def main():

	transferScripts('vm_test','stressAll.py')

	startVMLoad('vm_test',10,4,2,2,2,50,'stressAll.py')


#function to transfer scripts to VMs
def transferScripts(vm_name,script_name):


	#get the ip address of the target VM
	ip = getVM_ip(vm_name)
	#get the path to the script directories
	path = get_path(script_name)
	#where to send script inside vm
	vmPath = getVM_path(vm_name)

	#get access credentials
	user = get_user()
	password = get_password()

	
	if ip is None or path is None or user is None or password is None:
		print("Input Error")
		return False
	
	try:
		p = subprocess.call(['sshpass','-p',password,'scp','-o','StrictHostKeyChecking=no',path+'',user+'@'+ip+':'+vmPath])
		
		if(p==0):
			print("Scripts tansfered to ",vm_name)

		else:
			print("Connection Error ",vm_name)
			return False
	except Exception as e:
		print("Unknown erro")
		return False


# Start load on a VM
#vm - target vm name | cpu - num of VCPU | mem,disk,io - number of memory,disk,io workers (1-4) | util - utilization level (1-100) | script- target load script
# duration - in minutes (>= 1)
def startVMLoad(vm,duration,cpu,mem,disk,io,util,script):

	#get the ip address of the target VM
	ip = getVM_ip(vm_name)

	#get the path to the vm load script directory
	path = getVM_path(vm)


	#get access credentials
	user = get_user()
	password = get_password()

	if ip is None or path is None or user is None or password is None:
		print("Input Error")
		return False
	try:
		p = subprocess.Popen(['sshpass','-p',password,'ssh',user+'@'+ip,'python3  '+str(path)+'loadScriptName'+' '+str(cpu)+' '+str(io)+' '+str(mem)+' '+str(disk)+' '+str(util)+' '+str(duration*60)],stdout=subprocess.PIPE,universal_newlines=True)
		print("Load Started on VM",vm)
		return True

	except Exception as e:
		print("Load Failed:",p)
		return False


def getVM_ip(vm_name):
	print("Not implemented")

def get_path(script_name):
	print("Not implemented")

def getVM_path(vm_name):
	print("Not implemented")

def get_user():
	print("Not implemented")

def get_password():
	print("Not implemented")



if __name__ == '__main__':

	main()