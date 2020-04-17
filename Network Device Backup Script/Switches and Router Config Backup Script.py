import re #Library for regular expressions
import os
import time
import paramiko #Library to make ssh2 connections
import datetime
import telnetlib #Library to make telnet connections

###authentication details
USER = '<USERNAME>'
PASSWORD = '<PASSWORD>'

log_file_path = "<PATH-TO-LOG-FILE>"
if !os.path.exists(log_file_path):
		log_file = open(log_file_path, "a")

#Function for device access via SSH
#====================================================================================================================================

def ssh_devices(ssh_device_list) :
        counter_success = 0
        counter_fail    = 0
        fail_list = []

        for host_details in ssh_device_list.readlines():
                host_details = host_details.strip() #all leading and trailing white spaces are removed from the srting
                if re.match(r'^#',host_details) != None:
                        continue

                [vendor,host_name,host_ip] = host_details.split(",")

                folder_path ='<DIRECTORY-PATH-TO-STORE-CONFIG-BACKUPS>'+host_name
                NOW = datetime.datetime.now()
                filename = folder_path +'/'+host_name + '-' + NOW.strftime("%Y-%m-%d-%H-%M-%S")

                if (os.path.isdir(folder_path)): #check whether folder exists or not
                        pass
                else:
                        os.makedirs(folder_path)

                log_file.write('\n===========================================' + host_ip + '===========================================\n')
                log_file.write(NOW.strftime("%Y-%m-%d-%H-%M-%S") + ' - Connecting to the device : ' + host_ip + '.....\n')

                try:
                        session = paramiko.SSHClient() #A high-level representation of a session with an SSH server
                        session.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Set policy to use when connecting to servers
                                                                                	  #without a known host key
                        session.connect(host_ip, username=USER, password=PASSWORD) #Connect to an SSH server and authenticate 
                        device_access = session.invoke_shell() #Start an interactive shell session on the SSH server.
                        time.sleep(2) #Python time sleep function is used to add delay in the execution of a program.

                        NOW = datetime.datetime.now()
                        log_file.write(NOW.strftime("%Y-%m-%d-%H-%M-%S") + ' - Connected!!!\n')
                        log_file.write(NOW.strftime("%Y-%m-%d-%H-%M-%S")+ ' - Obtaining the device config.....\n')

                        if vendor == "cisco" or vendor == "planet":
                                device_access.send('terminal length 0\n') 
                                time.sleep(1)
                                device_access.send('show running-config\n') 
                                time.sleep(5)
                        elif vendor == "hp":
                                device_access.send('screen-length disable\n')
                                time.sleep(1)
                                device_access.send('display current-configuration\n')
                                time.sleep(5)
                        elif vendor == "huawei":
                                device_access.send('screen-length 0 temporary\n')
                                time.sleep(1)
                                device_access.send('display current-configuration\n')
                                time.sleep(5)

                        output = device_access.recv(999999)
                        # recv(nbytes) : Receive data from the channel. The return value is a string representing the data received.
                        #The maximum amount of data to be received at once is specified by nbytes.

                        NOW = datetime.datetime.now() #Return the current local date and time.
                        config_file = open(filename, 'a')
                        config_file.write(output)
                        config_file.close()

                        NOW = datetime.datetime.now() ###set date and time
                        log_file.write(NOW.strftime("%Y-%m-%d-%H-%M-%S") + ' - Config Successfully written!\n')
                        counter_success = counter_success+1
                except Exception as e:
                        NOW = datetime.datetime.now()
                        log_file.write(NOW.strftime("%Y-%m-%d-%H-%M-%S") + " - Could not obtain the config of " + host_ip + "\n")
                        log_file.write(str(e)+"\n")
                        counter_fail = counter_fail+1
                        fail_list.append("      " + str (host_ip) + "   " + str(host_name))

                        if os.path.exists(filename):
                                os.remove(filename)
                        continue #not sure needed this??
                finally:
                        session.close() #close session

        log_file.write("==========================================SUMMARY-SSH==============================================")
        log_file.write("\n\nTotal = str(counter_success+counter_fail), Successful = " + str(counter_success) + ", Faliures = " + str(counter_fail)+"\n")
        
        if fail_list != [] :
                log_file.write("Failed Device List  :\n")
                for entry in fail_list:
                        log_file.write(entry)
                        log_file.write("\n")
        log_file.write("\n")

#Function for devices access via telnet
#====================================================================================================================================

def telnet_devices(telnet_device_list):
        counter_success = 0
        counter_fail    = 0
        fail_list       = []
        for host_details in telnet_device_list.readlines():
                host_details = host_details.strip() 

                if re.match(r'^#',host_details) != None: #this allows to comment entries in the telnet device list file 
                        continue
                [vendor,host_name,host_ip] = host_details.split(",")

                folder_path ='<DIRECTORY-PATH-TO-STORE-CONFIG-BACKUPS>'+site+'/'+host_name
                NOW = datetime.datetime.now()
                filename = folder_path +'/'+host_name+'-'+NOW.strftime("%Y-%m-%d-%H-%M-%S")

                if (os.path.isdir(folder_path)): #check whether folder exists or not
                        pass
                else:
                        os.makedirs(folder_path)

                log_file.write('\n========================================' + host_ip + '========================================\n')
                log_file.write(NOW.strftime("%Y-%m-%d-%H-%M-%S") + ' - Connecting to the device : ' + host_ip + '.....\n')

                try:
                        telnet_session=telnetlib.Telnet(host_ip)
                        telnet_session.read_until("sername:",10) 
                        telnet_session.write(USER+ "\n")

                        telnet_session.read_until("assword:",5)
                        telnet_session.write(PASSWORD+ "\n")

                        NOW = datetime.datetime.now()
                        log_file.write(NOW.strftime("%Y-%m-%d-%H-%M-%S") + ' - Connected!!!\n')
                        log_file.write(NOW.strftime("%Y-%m-%d-%H-%M-%S") + ' - Obtaining the device config of ' + host_ip + ' .....\n')

                        if vendor == "cisco" :
                                telnet_session.write("terminal length 0\n")
                                telnet_session.write("show run\n")
                                telnet_session.write("exit\n")

                        output1 = []
                        while True:
                                try:
                                        line1 = telnet_session.read_until("\r\n",10)
                                        output1.append(line1)
                                except EOFError:
                                        break

                        output =  ''.join(output1)
                        telnet_session.close() #close session
                        
                        NOW = datetime.datetime.now() #Return the current local date and time.
                        config_file = open(filename, 'a')
                        config_file.write(output)
                        config_file.close()

                        NOW = datetime.datetime.now()
                        log_file.write(NOW.strftime("%Y-%m-%d-%H-%M-%S") + ' - Config Successfully written!\n')
                        counter_success += 1
                except Exception as e:
                        NOW = datetime.datetime.now()
                        log_file.write(NOW.strftime("%Y-%m-%d-%H-%M-%S") + " - Couldnt obtain the config of " +host_ip + "\n")
                        counter_fail = counter_fail+1
                        log_file.write(str(e)+"\n") #append the error into the log file
                        fail_list.append("      " + str (host_ip) + "   " + str(host_name))

                        if os.path.exists(filename):
                                os.remove(filename)
                        continue
                #finally:
                #        telnet_session.close() #close session

        log_file.write("\n==========================================SUMMARY-Telnet==============================================")
        log_file.write("\n\nTotal =" + str(counter_success+counter_fail)+ ", Successful = " + str(counter_success) + ", Faliures = " + str(counter_fail)+"\n")
        
        if fail_list != [] : #print the list of devices which were failed to logged into
                log_file.write("Failed Device List  :\n")
                for entry in fail_list:
                        log_file.write(entry)
                        log_file.write("\n")
        log_file.write("\n")

#Main  program
#====================================================================================================================================

if __name__ == "__main__":
        ssh_device_list    = open("<SSH-DEVICE-LIST-FILE-PATH>", "r")
        telnet_device_list = open("<TELNET-DEVICE-LIST-FILE-PATH>", "r")

        ssh_devices(ssh_device_list)
        telnet_devices(telnet_device_list)
        log_file.close()
        ssh_device_list.close()
        telnet_device_list.close()




