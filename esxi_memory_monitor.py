#####################################################################################################################################################                    
#                                                                                                                                                   #
# AUTHOR: JEROME SHEED                                                                                                                              #
# DATE: 28/11/2016                                                                                                                                  #                     
# PLATFORM: WINDOWS + PYTHON 2.7                                                                                                                    #
#                                                                                                                                                   #
# TAGS: ZABBIX, VMWARE, PYTHON                                                                                                                      #                      
#                                                                                                                                                   #                        
#####################################################################################################################################################
# EXPECTED OUTPUT:                                                                                                                                  #                       
#####################################################################################################################################################
#                                                                                                                                                   #                     
# Create a script to send memory values to Zabbix on a per host basis.                                                                              #
# Values to be determined via a powershell output file (esxi_memory.txt) that gets read in and used for this task.                                  #
#                                                                                                                                                   #                    
#####################################################################################################################################################
# VARIABLES:                                                                                                                                        #
#####################################################################################################################################################
#                                                                                                                                                   #                     
# zabbix_server = THE ZABBIX SERVER YOU ARE GOING TO REPORT IN TO.                                                         			    #
# free.memory = THE ITEM KEY YOU ARE REPORTING TO IN ZABBIX. THIS MUST EXIST IN ZABBIX - AS MUST THE HOST YOU ARE REPORTING ON.                     #
#                                                                                                                                                   #
#####################################################################################################################################################
# USAGE:                                                                                                                                            #
#####################################################################################################################################################
#                                                                                                                                                   #                     
# python esxi_memory_monitor.py                                                                                                                     #                       
#                                                                                                                                                   #                     
#####################################################################################################################################################
# TASKS PERFORMED:                                                                                                                                  #  
#####################################################################################################################################################
#                                                                                                                                                   #                     
# * READS POWERSHELL OUTPUT (FROM FILE esxi_memory_txt) AND PARSES FILE IN TO A DICTIONARY.                                                         #                       
# * DICTIONARY CONSISTS OF TWO COLUMNS - NAME AND USAGE.                                                                                            #                    
# * DICTIONARY READ IN AND USED TO PROVIDE INPUT TO "ZABBIX_SENDER" COMMAND.                                                                        #                   
#                                                                                                                                                   #                        
#####################################################################################################################################################
# REQUIREMENTS:                                                                                                                                     #                       
#####################################################################################################################################################
#                                                                                                                                                   #                     
# * WINDOWS                                                                                                                                         #                       
# * PYTHON 2.7                                                                                                                                      #
# * ZABBIX_SENDER.EXE (THIS CAN BE DOWNLOADED SEPERATELY OR PULLED FROM THE ZABBIX_AGENT PACKAGE)                            			    #
# * esxi_memory_txt FILE FOR PROCESSING                                                            						    #
#                                                                                                                                                   #
#####################################################################################################################################################
# SAMPLE esxi_memory_txt:                                                                                                                           #
#####################################################################################################################################################
#                                                                                                                                                   #
# Name                               TotalGB GrantedGB ConsumedGB ActiveGB Usage UsageActive                                                        #                    
# ----                               ------- --------- ---------- -------- ----- -----------                                                        #                    
# jerometest                 143,99  188,26    138,75     28,2377  96%    1Â 500%                                                                   #                      
#                                                                                                                                                   #                 
#####################################################################################################################################################

import subprocess

# CREATE VARIABLE TO ADD YOUR ZABBIX SERVER YOU ARE REPORTING TO HERE #
zabbix_server = "mgmt.zabbix.rsaweb.co.za"

# READ IN HOST / USAGE AND CREATE DICTIONARY #
f = open("esxi_memory.txt", 'r')
dictionary = {}

data = f.read()
data = data.split("\n")

for line in data:
    columns = line.split()
    columns[5] = columns[5].translate(None, '%')
    dictionary[columns[0]] = columns[5]

f.close()

# READ IN DICTIONARY AND PUBLISH TO ZABBIX VIA ZABBIX_SENDER #
for key, value in dictionary.iteritems():
    publish_free_memory = "zabbix_sender -z %s -s %s -k free.memory -o %s" %(zabbix_server, key, value)
    process = subprocess.Popen(publish_free_memory, shell = True, stdout=subprocess.PIPE)

# TROUBLESHOOT OUTPUT HERE IF NEEDED #
output,error = process.communicate()
    print output
