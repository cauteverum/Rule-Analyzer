import sqlite3, os 

class DB_MANAGEMENT: 
    def __init__(self): 
        pass

    def createDbForFw(self):
        try: 
            connection = sqlite3.connect("listenThis.db")
            cursor = connection.cursor()
            sql_command = "SELECT name from firewalls"
            cursor.execute(sql_command)
            data = cursor.fetchall()
            for d in data: 
                dbname = d[0] + '.db'
                if not os.path.exists(f"{dbname}"): 
                    table = f"""
                    CREATE TABLE "{d[0]}" (
                    "policyid" TEXT,
                    "srcip"	TEXT,
                    "dstip"	TEXT,
                    "dstport" TEXT,
                    "count" INTEGER
                    );
                    """
                    connection = sqlite3.connect(dbname)
                    cursor = connection.cursor()
                    cursor.execute(table)
        except: 
            pass

    def listen(self,name=str, ip=str):
        try:
            if not os.path.exists("listenThis.db"):
                table = """
                    CREATE TABLE IF NOT EXISTS "firewalls" (
                    "name"	TEXT NOT NULL UNIQUE,
                    "ip"	TEXT NOT NULL UNIQUE,
                    "exempt" TEXT);
                """
                connection = sqlite3.connect('listenThis.db')
                cursor = connection.cursor()
                cursor.execute(table)
                exempt = '0'
                insertQuery = "insert into firewalls (name,ip,exempt) VALUES (?,?,?)"
                values = (name,ip,exempt)
                cursor.execute(insertQuery, values)
                connection.commit()
                connection.close()
            else: 
                connection = sqlite3.connect('listenThis.db')
                cursor = connection.cursor()
                insertQuery = "insert into firewalls (name,ip) VALUES (?,?)"
                values = (name,ip)
                cursor.execute(insertQuery, values)
                connection.commit()
                connection.close()
        except: 
            print("This firewall is already in database")
    
    def showListendb(self): 
        connection = sqlite3.connect("listenThis.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * from firewalls")
        backToServer = []
        firewalls = cursor.fetchall()
        for f in firewalls: 
            backToServer.append(f[1])
        return backToServer


            
    def checklistenFw(self,ip): 
        connection = sqlite3.connect("listenThis.db")
        cursor = connection.cursor()
        # print(ip)
        cursor.execute("SELECT ip from firewalls WHERE ip = ?", (ip,))
        lenght = cursor.fetchall()
        # print(f"Lenght: {lenght}")
        if len(lenght) > 0: 
            # print("Return True")
            return True
        else: 
            # print("Return False")
            return False
    
    def exempt(self,fname=str, exemptPolicies=str): 
        connection = sqlite3.connect("listenThis.db")
        cursor = connection.cursor()
        cursor.execute(f"""
                    UPDATE firewalls SET exempt = ? where (name = ?)
                """, (exemptPolicies, fname))
        connection.commit()


    def checkExempt(self, fname=str): 
        connection = sqlite3.connect("listenThis.db")
        cursor = connection.cursor()
        cursor.execute("""
            SELECT exempt FROM firewalls where (name = ?)
        """,(fname,))
        result = cursor.fetchone()
        return result[0].split(',')

