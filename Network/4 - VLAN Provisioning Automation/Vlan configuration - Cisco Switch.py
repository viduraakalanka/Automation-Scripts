import re #Library for regular expressions
import time
import paramiko #Library to make ssh2 connections

#Firewall authentication details
#===================================================================================================================================

SW1_IP      = '192.168.1.1'
SW2_IP      = '192.168.1.2'


TACACS_USER      = 'USER'
TACACS_PASSWORD  = 'PW'

#Function to enable SSH_login
#====================================================================================================================================

def ssh_login(IP,USER,PASSWORD):
    session = paramiko.SSHClient() #A high-level representation of a session with an SSH server
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    session.connect(IP, username=USER, password=PASSWORD) #Connect to an SSH server and authenticate 
    device_shell = session.invoke_shell() #Start an interactive shell session on the SSH server.
    time.sleep(2) #Python time sleep function is used to add delay in the execution of a program.
    return session,device_shell

    
#Function to access devices via SSH
#====================================================================================================================================

def switch_config(vlan_id, vlan_name) :

    try:
        #Leaf1 Configuration
        #-----------------------------------------------------------------------------------
        session,device_shell = ssh_login(SW1_IP, TACACS_USER, TACACS_PASSWORD)
        
        print("Connected to Cisco switch....")        
        print("Configuring Cisco switch...")

        #VLAN Config
        device_shell.send("configure terminal\n")
        time.sleep(1)
        device_shell.send("vlan  " + vlan_id + "\n")
        time.sleep(1)
        device_shell.send("name  " + vlan_name + "\n")
        time.sleep(1)
        device_shell.send('exit\n')
        time.sleep(1)

        #Allowing vlan in Eth1/6
        print ("Configure vlan in interfaces")
        device_shell.send("interface Ethernet1/6\n")
        time.sleep(1)
        device_shell.send("switchport trunk allowed vlan add  " + vlan_id + "\n")
        time.sleep(1)
        device_shell.send('exit\n')
        time.sleep(1)

        #Allowing vlan in port channel 10
        device_shell.send("interface port-channel10\n")
        time.sleep(1)
        device_shell.send("switchport trunk allowed vlan add  " + vlan_id + "\n")
        time.sleep(1)
        device_shell.send('exit\n')
        time.sleep(1)

        session.close()
        output = device_shell.recv(999999)
        print (output) #Print switch output for troubleshooting

        #Leaf2 Configuration
        #-----------------------------------------------------------------------------------
        session,device_shell = ssh_login(SW2_IP, TACACS_USER, TACACS_PASSWORD)
        
        print("Connected to Cisco switch....")        
        print("Configuring Cisco switch...")

        #VLAN Config
        device_shell.send("configure terminal\n")
        time.sleep(1)
        device_shell.send("vlan  " + vlan_id + "\n")
        time.sleep(1)
        device_shell.send("name  " + vlan_name + "\n")
        time.sleep(1)
        device_shell.send('exit\n')
        time.sleep(1)

        #Allowing vlan in Eth1/5
        print ("Configure vlan in interfaces")
        device_shell.send("interface Ethernet1/5\n")
        time.sleep(1)
        device_shell.send("switchport trunk allowed vlan add  " + vlan_id + "\n")
        time.sleep(1)
        device_shell.send('exit\n')
        time.sleep(1)

        #Allowing vlan in port channe30
        device_shell.send("interface port-channel30\n")
        time.sleep(1)
        device_shell.send("switchport trunk allowed vlan add  " + vlan_id + "\n")
        time.sleep(1)
        device_shell.send('exit\n')
        time.sleep(1)

        session.close()
        output = device_shell.recv(999999)
        print (output) #Print switch output for troubleshooting

       
        print("Switch configuration complete....")
                    
    except Exception as e:
        print (str(e))

#Main method
#=================================================================================================================================

if __name__ == "__main__":
    vlan_id   = input ("Enter vlan id               : ")
    vlan_name = input ("Enter vlan name (No spaces) : ")        
    switch_config(vlan_id,vlan_name)
        
