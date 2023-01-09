from sys import argv
from dbManagement import DB_MANAGEMENT
from os import system
system("color 0C")
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


        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        """
        print(info)
    elif ("--add" in argument) and ('-f' in argument) and ('-i' in argument): 
        idx = argument.index("--add")
        name = argument[idx+2]
        ip = argument[idx+4]
        ch = input(f"Name: {name} ip address: {ip}\nDo you want to continue?(y/n): ")
        if ch.lower() == 'y': 
            instance_DBM.listen(name=name, ip=ip)
            instance_DBM.createDbForFw()
            print("[DONE]")

    elif ("ls" in argument): 
        result = instance_DBM.showListendb()
        for i in result: 
            print(i)
    
    elif ("--exempt" in argument): 
        try:
            idx = argument.index("--exempt")
            fname = argument[idx+2]
            exemptPolicies = argument[idx+4]
            instance_DBM.exempt(fname=fname, exemptPolicies=exemptPolicies)
            print("[DONE]")
        except: 
            pass

if __name__ == '__main__': 
    management()
