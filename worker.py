import sqlite3
class JOB: 
    def __init__(self): 
        pass

    @staticmethod
    def parser(text=str, exemptPolicy = []): 
        text = text.split()
        policyid, srcip, dstip, dstport = '', '', '', ''
        for t in text: 
            if 'subtype=' in t: subtype = t.split('=')[1]                
            elif 'devname=' in t: devname = t.split('=')[1]               
            elif 'policyid=' in t: policyid = t.split('=')[1]              
            elif 'srcip=' in t: srcip = t.split('=')[1]               
            elif 'dstip=' in t: dstip = t.split('=')[1]                
            elif 'dstport=' in t: dstport = t.split('=')[1]
                
        
        connection = sqlite3.connect("listenThis.db")
        cursor = connection.cursor()
        cursor.execute("""
            SELECT exempt from firewalls where (name = ?)
        """, (devname,))
        exemptPolicy = cursor.fetchone()[0].split(',')
        connection.close()

        if (dstport != '') and (policyid != '0') and (subtype == '"forward"') and (not policyid in exemptPolicy): 
            dbname = str(devname).strip('""') + '.db'
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
                print("ELSE CONDITION WORKED")
                cursor.execute(f"""
                    INSERT INTO {devname} (policyid, srcip, dstip, dstport, count) VALUES (?,?,?,?,?)
                """, (policyid, srcip, dstip, dstport, 1))
                connection.commit()
            connection.close()


