import re #Library for regular expressions
import time
import paramiko #Library to make ssh2 connections

#Firewall authentication details
#===================================================================================================================================

FW1_IP        = 'IP'
FW1_USER      = 'USER'
FW1_PASSWORD  = 'PW'

FW2_IP        = 'IP'
FW2_USER      = 'USER'
FW2_PASSWORD  = 'PW'

#Function to extract unique IP addresses
#====================================================================================================================================

def find_unique():
    with open('2-Dup_Val.txt', 'r') as f:
        dup_ip_list = [line.strip() for line in f]  #removes both leading and trailing specified characters

    dup_ip_list = [line.replace("[.]",".") for line in dup_ip_list] #remove brackets
        
    uniq_ip_list = list(set(dup_ip_list))
    print(uniq_ip_list)
    print('\n\n\n')
    output_file = open('3-Unique_Val.txt','w')
    for ip in uniq_ip_list:
        output_file.write(str(ip)+"\n")

    output_file.close()
    return uniq_ip_list


#Function to enable SSH_login
#====================================================================================================================================

def ssh_login(IP,USER,PASSWORD):
    session = paramiko.SSHClient() #A high-level representation of a session with an SSH server
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Set policy to use when connecting to servers
                                                                                	  #without a known host key
    session.connect(IP, username=USER, password=PASSWORD) #Connect to an SSH server and authenticate 
    device_shell = session.invoke_shell() #Start an interactive shell session on the SSH server.
    time.sleep(2) #Python time sleep function is used to add delay in the execution of a program.
    return session,device_shell

    
#Function to access devices via SSH
#====================================================================================================================================

def vdom_config(vdom_list) :
    login_state = False
    ADDRESS_GRP_NAME = 'GRP_NAME'
    
    uniq_ip_list = find_unique()
    ip_string = ''
    for ip_address in uniq_ip_list :
        ip_string = ip_string + '\"'+ ip_address + '\" '
    print (ip_string)

    for vdom_details in vdom_list.readlines():
        
        vdom_details = vdom_details.strip() #all leading and trailing white spaces are removed from the srting
        [site,vdom_name] = vdom_details.split(",")
        
        if re.match(r'^#',site) != None:
            continue

        try:
            if site == 'FW1' and login_state == False:
                session,device_shell = ssh_login(FW1_IP, FW1_USER, FW1_PASSWORD)
                print("Connected to "+ site + "....")
                login_state  = True    
            elif site == 'FW2' and login_state == False:
                session,device_shell = ssh_login(FW2_IP, FW2_USER, FW2_PASSWORD)
                print("Connected to "+ site + "....")
                login_state = True
            elif site == "NULL" and login_state == True: #This is needed to login from one FW to the other
                login_state = False
                print("Disconnected from "+ site + "....")
                session.close()
                
            print("Configuring "+ vdom_name + " vdom")

            #Logging into the firewall and then to vdom
            device_shell.send('config vdom \n')
            time.sleep(1)
            device_shell.send('edit \"' + vdom_name + '\" \n')
            time.sleep(1)
            device_shell.send('config firewall address \n')
            time.sleep(1)
            print("Configuring Addresses....")
            
            for ip_address in uniq_ip_list :
                device_shell.send('edit \"' + ip_address + '\" \n') 
                time.sleep(1)
                device_shell.send('set subnet \"' + ip_address + '\" \"255.255.255.255\" \n') 
                time.sleep(1)
                #device_shell.send('set visibility enable \n') 
                #time.sleep(1)
                device_shell.send('next \n') 
                time.sleep(1)
                print("Address "+ ip_address + " configured")
                
            device_shell.send('end \n')
            time.sleep(1)

            #configuring Address Block
            print("Configuraing Address Group....")
            device_shell.send('config firewall addrgrp \n')
            time.sleep(1)
            device_shell.send('edit \"' + ADDRESS_GRP_NAME + '\" \n')
            time.sleep(1)
            device_shell.send('append member ' + ip_string + ' \n')
            time.sleep(1)
            device_shell.send('next \n')
            time.sleep(1)
            device_shell.send('end \n')
            time.sleep(1)
            device_shell.send('next \n')
            time.sleep(1)
            print("Address Group configured")
    
        except Exception as e:
            print (str(e))
        finally:
            session.close() #close session

#Main method
#=================================================================================================================================

if __name__ == "__main__":
        vdom_list = open("4-VDOM_LIST.txt",'r')
        vdom_config(vdom_list)
        vdom_list.close()
        





