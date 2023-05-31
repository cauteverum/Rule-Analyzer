import pandas as pd 
from sys import platform
from os import system


def clearScreen(): 
    if platform == "linux" or platform == "linux2": 
        system("clear")
    elif platform == "darwin": 
        system("clear")
    elif platform == "win32": 
        system("cls")


def calculatePercentage(total:int,current:int): 
    percentage = int((current/total)*100)
    sharp = "#"*percentage
    dash = "-"*(100-percentage)
    bar = sharp+dash
    if platform == "linux" or platform == "linux2": 
        system("clear")
        print(bar)
        print(f"Calculating... %{percentage}")
    elif platform == "darwin": 
        system("clear")
        print(bar)
        print(f"Calculating... %{percentage}")
    elif platform == "win32": 
        print(bar)
        system("cls")
        print(f"Calculating... %{percentage}")


def get_content_convert_list(): 
    try:
        fname = input("File name: ")
        content = ""
        with open(file=fname, mode="r",encoding="utf-8") as file: 
            content = file.read()
            content = content.split("\n")
        
        return content
    except KeyboardInterrupt: 
        print("\n\nForced to shut down")


def create_json_convert_pandasDF(logs:list): 
    try: 
        policyids, srcips, dstips, dstports = [],[],[],[]
        jsonFormat = {
            "policyid":policyids,
            "srcip":srcips,
            "dstip":dstips,
            "dstport":dstports,
            "count":1
        }
        for sublist in logs: 
            sublist = sublist.split()
            global srcip, dstip,dstport,policyid
            policyid, srcip, dstip,dstport = "","", "",""
            for value in sublist: 
                
                value = value.strip("''")
                if "policyid=" in value and "shapingpolicyid=" not in value: 
                    policyid = value.split("=")[1]
                elif "srcip=" in value: 
                    srcip = value.split("=")[1]
                elif "dstip=" in value: 
                    dstip = value.split("=")[1]
                elif "dstport=" in value: 
                    dstport = value.split("=")[1]
                else: pass

                if policyid and srcip and dstip and dstport: 
                    policyids.append(policyid)
                    srcips.append(srcip)
                    dstips.append(dstip)
                    dstports.append(dstport)
                
        df = pd.DataFrame.from_dict(jsonFormat)
        return df
    except: 
        pass


def operation(df):
    try:
        usage = 0
        weight = float(input("Data was converted into Pandas DataFrame. \nType x% weight for calculating more specific policy:  ")) 
        exempt = input("Exempt For Policies (you can leave here blank or type a list or just a policy [For Instance:1 2 3]):").split()
        policies = df["policyid"].unique()
        clearScreen()
        print("-"*100 + "\n" + "Calculating... %0") 
        fullText = ""
        row_count = len(df.index)
        with open(file="result.txt", mode='w',encoding='utf-8') as file: 
            file.write('')

        for pol in policies:
            if pol != '0' and pol not in exempt: 
                totalUsage = df[df["policyid"] == pol]["count"].sum()
                srcipUnique = df[(df["policyid"]==pol)]["srcip"].unique()
                dstipUnique = df[(df["policyid"]==pol)]["dstip"].unique()
                dstportUnique = df[(df["policyid"]==pol)]["dstport"].unique() 
                usage = usage + totalUsage
        
                for src in srcipUnique: 
                    count = df[ (df["policyid"]==pol)  & (df["srcip"]== src)]["count"].sum() 
                    if count/totalUsage > weight/100: 
                        fullText = fullText + f"policy:{pol} srcip:{src} used {count} times proportionally: % {round((count/totalUsage)*100, 3)}" + '\n' 
                for dst in dstipUnique: 
                    count = df[ (df["policyid"]==pol)  & (df["dstip"]== dst)]["count"].sum()    
                    if count/totalUsage > weight/100: 
                        fullText = fullText + f"policy:{pol} dstip:{dst} used {count} times proportionally: % {round((count/totalUsage)*100, 3)}" +'\n' 
                for dstport in dstportUnique: 
                    count = df[ (df["policyid"]==pol)  & (df["dstip"]== dst)]["count"].sum()    
                    if count/totalUsage > weight/100: 
                        fullText = fullText + f"policy:{pol} dstport:{dstport} used {count} times proportionally: % {round((count/totalUsage)*100, 3)}" +'\n'  

                with open(file="result.txt",mode='a',encoding='utf-8') as file: 
                    file.write(f"Policy:{pol} src unique:{len(srcipUnique)} destination unique:{len(dstipUnique)} dport unique:{len(dstportUnique)}\n" + fullText.strip() + '\n\n\n')
                fullText = ''
                calculatePercentage(row_count,usage)
        clearScreen()
        print("#"*100)
        print("Calculating... %100")
    
    except KeyboardInterrupt: 
        print("\n\nForced to shut down")



clearScreen()
content = get_content_convert_list()
df = create_json_convert_pandasDF(content)
operation(df)