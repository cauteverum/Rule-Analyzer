from sys import argv
from dbManagement import DB_MANAGEMENT
from sys import platform
from os import system


if platform == "win32": 
   system("color 0A")

instance_DBM = DB_MANAGEMENT()
def management(): 
    argument = argv
    if "--help" in argument: 
        info = """
        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

                                HELP

              ls        ------> list your firewall and their ip addresses. 
            --help      ------> Help Menu   
            --add       ------> Add a firewall for syslog server to listen.
        (format for --add ----> --add -f 'name of firewall' -i 'ip address of firewall')
            --exempt ---------> (format: --exempt -f 'firewall name' -ex 1,2,3)
            --storedlog ------> if you've logs stored on your local machine you can use this argument to analyz data.
  (format for --storedlog ---->  manage.py --storedlog
                               


        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        """
        print(info)
    
    elif ("--storedlog" in argument): 
        try: 
            if platform == "linux" or platform == "linux2": 
                system("python3 storedLogs.py")
            elif platform == "darwin": 
                system("python3 storedLogs.py")
            elif platform == "win32": 
                system("python storedLogs.py")
        except Exception as err: 
            print(f"Error: \n{err}")

    elif ("--add" in argument) and ('-f' in argument) and ('-i' in argument): 
        try:
            idx = argument.index("--add")
            name = argument[idx+2]
            ip = argument[idx+4]
            ch = input(f"Name: {name} ip address: {ip}\nDo you want to continue?(y/n): ")
            if ch.lower() == 'y': 
                instance_DBM.listen(name=name, ip=ip)
                instance_DBM.createDbForFw()
                print("[DONE]")
        except:
            print("[Syntax Error]")
            
    elif ("ls" in argument):
        try:
            result = instance_DBM.showListendb()
            for i in result: 
                print(i)
        except:
            print("There is no data to list")
    
    elif ("--exempt" in argument): 
        try:
            idx = argument.index("--exempt")
            fname = argument[idx+2]
            exemptPolicies = argument[idx+4]
            instance_DBM.exempt(fname=fname, exemptPolicies=exemptPolicies)
            print("[DONE]")
        except: 
            print("[Syntax Error] use --help command to understand how to use --exempt argument")

if __name__ == '__main__': 
    management()
