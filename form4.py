from urllib.request import urlopen
from lxml import etree
import threading
import re
import mariadb
import sys
import requests
import unicodedata
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import json
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

s = requests.Session()


global today
global filing_date
global lookback_date
today = datetime.now().date()
filing_date = (datetime.now() - timedelta(days=1)).date()
lookback_date = (datetime.now() - timedelta(days=14)).date()

def _establishDBConn():
        try:
            global conn
            conn = mariadb.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT")),
                database=os.getenv("DB_DB")
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        def _establishheaders():
            global payload
            global headers
            payload={}
            headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="87", ""Not;A\\Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'en-US,en;q=0.9'
            }

        global cursor
        cursor = conn.cursor()
        _establishheaders()
        

def _parsing_f4_data():
    i = 0
    while i < 10:
        c = i * 100
        d = c + 100
        url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=4&company=&dateb=&owner=include&start={}&count={}&output=atom".format(c,d)
 
        response =  s.request("GET", url, headers=headers, data = payload).text
        soup = BeautifulSoup(response, 'lxml')
        entries = soup.find_all('entry')

        cursor.execute("SELECT * FROM form4") 
        global data
        data = cursor.fetchall ()
        
        for entry in entries:           
            cik_data = entry.find('title').text[4:] 
            if 'Issuer' in cik_data:
                
                date_of_filing = entry.find('updated').text[:10]
                if str(date_of_filing) == str(today) or str(date_of_filing) == str(filing_date):
                    a = cik_data.split('(')
                    ciknumbers = a[1][0:10]
                    accountname = a[0]
                    try:
                        cursor.execute("INSERT INTO form4 (Issuer, CIKNumber, Date) VALUES (?, ?, ?)", (accountname,ciknumbers,date_of_filing)) 
                        conn.commit() 
                    except mariadb.Error as e:
                        print(f"Error: {e}")
                else:
                    i = 50000
                    print('wrong date')
        if entries == []:
            i = 50000
        if i < 50000:
            i = i + 1
        print(f"Set Completed: {i}")
    cursor1 = conn.cursor()
    cursor1.execute("""SELECT 
        CIKNumber, COUNT(CIKNumber)
    FROM
        form4
    GROUP BY 
        CIKNumber
    HAVING 
        COUNT(CIKNumber) > 1;""")

    cursor1.execute("""DELETE t1 FROM form4 t1
    INNER JOIN form4 t2 
    WHERE 
        t1.id < t2.id AND 
        t1.CIKNumber = t2.CIKNumber;""")
    conn.commit()




def _scraping_f4_activity():
    
    cursor.execute("""SELECT * FROM form4""")
    results = cursor.fetchall()

    cursor.execute("""SELECT CIKNumber, Issuer FROM form4""")
    companydict = {}
    for (CIK,issuer) in cursor:
        companydict[CIK] = issuer



    j = 0
    for row in results:
        ownerlist = []
        ownerdesclist = []
        cik_for_search = row[2]        
        url_2 = 'https://www.sec.gov/cgi-bin/own-disp?action=getissuer&CIK={}'.format(cik_for_search)
        response_2 = s.request("GET", url_2, headers=headers, data = payload).text
        soup_2 = BeautifulSoup(response_2, 'lxml')
        tables = soup_2.find_all('table')
        # print(tables[6])
        try:
            names = [tr.extract() for tr in tables[6].find_all("tr")][1:]
            for name in names:
                itemizedrow1 = [td.extract() for td in name.find_all("td")]
                ownerlist.append(str(itemizedrow1[0])[str(itemizedrow1[0]).find('CIK')+4:str(itemizedrow1[0]).find('CIK')+14])
                ownerdesclist.append(str(itemizedrow1[3])[str(itemizedrow1[3]).find('<td>')+4:str(itemizedrow1[3]).find('</td>')])
            ownerdict = dict(zip(ownerlist, ownerdesclist))

            secondtable = soup_2.find(attrs={"id": "transaction-report"})

            items = [tr.extract() for tr in secondtable.find_all("tr")]
            i = 1
            while i < len(items): 
                try:
                    itemrowinSecondTable = items[i]
                    itemizedrow = [td.extract() for td in itemrowinSecondTable.find_all("td")]
                    transactiontype = re.split(r'[><]',str(itemizedrow[5]))[2]
                    try:
                        dateofevent = datetime.strptime(re.split(r'[><]',str(itemizedrow[1]))[2], '%Y-%m-%d').date()
                    except:
                        dateofevent = "NULL"
                    fullname = re.split(r'[><]',str(itemizedrow[3]))[2]
                    ownerCIK = re.split(r'[><]',str(itemizedrow[10]))[2]
                    secname = re.split(r'[><]',str(itemizedrow[11]))[2]
                    numberofsectrans = re.split(r'[><]',str(itemizedrow[7]))[2]
                    numberofsectrans = int(re.split(r'[.]',numberofsectrans)[0].strip())
                    numberofsecowned = re.split(r'[><]',str(itemizedrow[8]))[2]
                    numberofsecowned = int(re.split(r'[.]',numberofsecowned)[0].strip())
                    try:
                        percentChange = (numberofsectrans/numberofsecowned)*100
                    except:
                        percentChange = None



                    if dateofevent > lookback_date:
                        try:
                            cursor.execute("""INSERT INTO scrapeddata (CIKNumber, DateofEvent, TransactionType, FullName, ownerCIK, secName, numberowned, numbertrans, percentChange, ownerdesc, issuer) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (cik_for_search,str(dateofevent),transactiontype,fullname,ownerCIK, secname, numberofsecowned, numberofsectrans,percentChange,str(ownerdict[ownerCIK]),companydict[cik_for_search]))
                            conn.commit() 
                        except mariadb.Error as e:
                            print(f"Error: {e}")
                    else:
                        break
                except:
                    pass    
                i = i + 1
        except:
            pass





def calcuniquedata():
    dfn = pd.read_sql("SELECT * FROM scrapeddata",conn,index_col="ID")

    dfncol = list(dfn.columns.values)
    dfnn = pd.DataFrame(columns=dfncol)


    for compCIK in dfn.CIKNumber.unique():
        # print(dfn.loc[j,['ownerCIK']].values[0])

        dfb = dfn[dfn['CIKNumber'] == compCIK]
        for item in dfb.ownerCIK.unique():    
            dfbb = dfb[dfb['ownerCIK'] == item]


            dfnn = dfnn.append(dfbb[dfbb['numberowned'] == dfbb['numberowned'].max()])
            dfnn = dfnn.append(dfbb[dfbb['numberowned'] == dfbb['numberowned'].min()])
    dfnn = dfnn.drop_duplicates(keep='first')    

    for row in dfnn.itertuples():
        try:
            cursor.execute("""INSERT INTO uniquedata (CIKNumber, DateofEvent, TransactionType, FullName, ownerCIK, secName, numberowned, numbertrans, percentChange) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (row.CIKNumber,row.DateofEvent,row.TransactionType,row.FullName,row.ownerCIK, row.secName, row.numberowned, row.numbertrans,row.percentChange))
            conn.commit() 
        except mariadb.Error as e:
            print(f"Error: {e}")






def exporttocsv():
    dfcsv = pd.read_sql("SELECT * FROM scrapeddata",conn,index_col="ID")
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    now = datetime.now()
    now = now.strftime("%m %d %Y")
    dfcsv.to_csv(desktop + '\\Report ' + now + ".csv")














def _filtering_data():
    placeholder = 1 
    """
    This is where the software will filter out the data to find out if its relevant 
    using the date to consider the relevancy and the criteria - this is the sale, puchase thing
    """



"""
# def _export_relevant_data_to_xcel():
#     placeholder = 1
#     
#     this is where the final relevant data will go for the analyst - or us, to write the report that will go out daily 

#     columns that will include - 'issuer', 'cik', 'url', and notes 
#     """





t0 = threading.Thread(target=_establishDBConn)
t1 = threading.Thread(target=_parsing_f4_data)
t2 = threading.Thread(target=_scraping_f4_activity)
t3 = threading.Thread(target=calcuniquedata)
t4 = threading.Thread(target=exporttocsv)
t0.start()
t0.join()

t1.start()
t1.join()
t2.start()
t2.join()
t3.start()
t3.join()
t4.start()
t4.join()
