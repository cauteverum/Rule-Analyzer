import threading
from server import SYSLOGSERVER
from worker import JOB
from time import sleep


def reportFunction(): 
    while True:
        sleep(20)
        print("Report Thread worked")
        firewalls = JOB.detectFirewalls()
        for firewall in firewalls: 
            print(firewall)
            JOB.calculate(firewall)
    
instance = SYSLOGSERVER()
serverThread = threading.Thread(target=instance.start)
reportThread = threading.Thread(target=reportFunction)



if __name__ == '__main__': 
    reportThread.start()
    serverThread.start()
