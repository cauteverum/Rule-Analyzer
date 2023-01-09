import socket
from dbManagement import DB_MANAGEMENT
from worker import JOB

class SYSLOGSERVER: 
    def __init__(self): 
        self.PORT = 514
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.BREAK = False
        self.FORMAT = 'utf-8'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(self.ADDR)
        self.instance_DBM = DB_MANAGEMENT()



    def start(self): 
        listen = self.instance_DBM.showListendb()
        # print(listen)
        print(f"[LISTENING] server is listening on {self.SERVER}:{self.PORT}")
        while not self.BREAK: 
            message , addr = self.server.recvfrom(1024)
            message = str(message.decode(self.FORMAT))
            print(message)
            if addr[0] in listen: 
                print('IM HERE')
                print(addr, message)
                JOB.parser(message)

