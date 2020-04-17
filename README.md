# Network Device Configuration Backup Automation

This repository contains a python script to automate Cisco, Huawei, HP switch and router configuration backups. Works for devices which can be logged in via Telnet anad SSH. Log file indicates successful and failed backups. To use this script edit following places in the code.

       1. Line   9 : Include username
       2. Line  10 : Include Password
       3. Line  12 : Log file path
       4. Line  31 : Set backup folder path for devices access via SSH
       5. Line 120 : Set backup folder path for devices access via Telnet
       6. Line 195 : Set path for file containing ssh devices list
       7. Line 196 : Set path for file containing telnet devices list

Note : SSH and Telnet Device list file format - 

              - 'vendor,host_name,host_ip'
              - Use '#' at the begining of the line for commenting
              
