import sqlite3
from dbManagement import DB_MANAGEMENT

import pandas as pd 
class JOB: 
    def __init__(self): 
        pass
    
    @staticmethod
    def detectFirewalls(): 
        connection = sqlite3.connect("listenThis.db")
        cursor = connection.cursor()
        cursor.execute("SELECT name from firewalls")
        result = cursor.fetchall()
        firewalls = []
        for res in result: 
            firewalls.append(res[0])
        return firewalls

    @staticmethod
    def calculate(db):
        dbname = db + '.db'
        connection = sqlite3.connect(dbname)
        df = pd.read_sql_query(f"SELECT * FROM {db}", connection)
        policies = df["policyid"].unique()
        fullText = ''
        fileName = db + '.txt'
        with open(file=fileName, mode='w',encoding='utf-8') as file: 
            file.write('')
        for pol in policies: 
            totalUsage = df[df["policyid"] == pol]["count"].sum()
            srcipUnique = df[(df["policyid"]==pol)]["srcip"].unique()
            dstipUnique = df[(df["policyid"]==pol)]["dstip"].unique()
            dstportUnique = df[(df["policyid"]==pol)]["dstport"].unique()

            for src in srcipUnique: 
                count = df[ (df["policyid"]==pol)  & (df["srcip"]== src)]["count"].sum()     
                if count/totalUsage > 0.1: 
                    fullText = fullText + f"policy:{pol} srcip:{src} used {count} times proportionally: % {round((count/totalUsage)*100, 3)}" + '\n'   
            for dst in dstipUnique: 
                count = df[ (df["policyid"]==pol)  & (df["dstip"]== dst)]["count"].sum()     
                if count/totalUsage > 0.1: 
                    fullText = fullText + f"policy:{pol} dstip:{dst} used {count} times proportionally: % {round((count/totalUsage)*100, 3)}" +'\n'         
            for dstport in dstportUnique: 
                count = df[ (df["policyid"]==pol)  & (df["dstport"]== dstport)]["count"].sum()     
                if count/totalUsage > 0.1:
                    fullText = fullText + f"policy:{pol} dstport:{dstport} used {count} times proportionally: % {round((count/totalUsage)*100, 3)}" +'\n'             
            with open(file=fileName,mode='a',encoding='utf-8') as file: 
                file.write(f"Policy:{pol} src unique:{len(srcipUnique)} destination unique:{len(dstipUnique)} dport unique:{len(dstportUnique)}\n" + fullText.strip() + '\n\n\n')
            fullText = ''


    @staticmethod
    def parser(text=str): 
        text = text.split()
        policyid, srcip, dstip, dstport = '', '', '', ''
        for t in text: 
            if 'subtype=' in t: subtype = t.split('=')[1].strip('""')             
            elif 'devname=' in t: devname = t.split('=')[1].strip('""')           
            elif 'policyid=' in t: policyid = t.split('=')[1]              
            elif 'srcip=' in t: srcip = t.split('=')[1]               
            elif 'dstip=' in t: dstip = t.split('=')[1]                
            elif 'dstport=' in t: dstport = t.split('=')[1]


    
        exemptPolicy = DB_MANAGEMENT().checkExempt(devname)
        if (dstport != '') and (policyid != '0') and (subtype == 'forward') and (not policyid in exemptPolicy): 
            dbname = str(devname) + '.db'
            connection = sqlite3.connect(dbname)
            cursor = connection.cursor()
            cursor.execute(f"""
                SELECT * FROM {devname} where (policyid = ? and srcip = ? and dstip = ? and dstport = ?)
            """, (policyid, srcip, dstip, dstport))
            duplicate = cursor.fetchall()
            

            if len(duplicate) > 0: 
                cursor.execute(f"""
                    SELECT count FROM {devname} where (policyid = ? and srcip = ? and dstip = ? and dstport = ?)
                """, (policyid, srcip, dstip, dstport))
                count = cursor.fetchone()[0]
                count += 1
                cursor.execute(f"""
                    UPDATE {devname} SET count = ? where (policyid = ? and srcip = ? and dstip = ? and dstport = ?)
                """, (count, policyid, srcip, dstip, dstport))
                connection.commit()
                
            else: 
                cursor.execute(f"""
                    INSERT INTO {devname} (policyid, srcip, dstip, dstport, count) VALUES (?,?,?,?,?)
                """, (policyid, srcip, dstip, dstport, 1))
                connection.commit()
            connection.close()

