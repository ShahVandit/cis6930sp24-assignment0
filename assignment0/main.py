import requests
import pypdf
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve
import sqlite3
import os
import argparse

def main(url):

    # Extract data
    incidents = extractincidents(url)
	
    # Create new database
    db, cursor = createdb()
	
    # Insert data
    populatedb(db, incidents)
	
    # Print incident counts
    status(db)

def fetchincidents(url):
    headers = {}
    headers[
        "User-Agent"
    ] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    
    response = requests.get(url, headers=headers)
    pdf_urls=[]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        heading = soup.find_all('div', class_='paragraph paragraph--type--accordion-group')[0]
    #     for head in heading:
        months=heading.find_all('div', class_='accordion-item')
        for month in months:
            daily=month.find_all('p')
            i=2
            while(i<len(daily)):
                pdf_get = requests.get("https://www.normanok.gov"+daily[i].find('a')['href'], 'wb')
                pdf_urls.append('https://www.normanok.gov'+daily[i].find('a')['href'])  
                i+=3

    else:
        print(f"Failed to retrieve PDF: Status code {response.status_code}")
    return pdf_urls

# def deletedb():


def extractincidents(pdf_url):
    rx = r"\s+(?=\d+/\d+/\d+\s)"
    l=0
    incidents=[]
    # for pdf_url in pdf_urls:
    urlretrieve(pdf_url,str(l)+'.pdf')
    with open(str(l)+'.pdf', 'rb') as file:
            pdf_reader = pypdf.PdfReader(str(l)+'.pdf')
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text(extraction_mode="layout")
                text+="\n\n\n"
                text=text.strip(r'\s{2,}')
    text=re.split(rx,text)
    i=0
    while(i<len(text)-2):
        text[i]=re.findall(rx,text[i])
        parts = re.split(r'\s{2,}', text[i+1], maxsplit=4)
        if(len(parts)==5):
            temps={'incident_time':parts[0], 'incident_number':parts[1], 'incident_location':parts[2], 'nature':parts[3], 'incident_ori':parts[4]}
        else:
            temps={'incident_time':parts[0], 'incident_number':parts[1], 'incident_ori':parts[2], 'nature':'', 'incident_location':''}
        i+=1
        incidents.append(temps)
    l+=1
    return incidents
def printIncidents(incidents):
    for incident in incidents:
        print(incident['incident_time'])

def createdb():
    # Create directory if it doesn't exist
    if not os.path.exists("resources"):
        os.makedirs("resources")
    
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect("resources/normanpd.db")
    
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # Create the 'incidents' table with the specified schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    
    # Commit changes
    # conn.commit()
    
    # Return the database connection
#     conn.close()
    return (conn,cursor)

def populatedb(db, incidents):
#     connection_obj = sqlite3.connect('normanpd.db')
    # deletedb(db=db)
    # cursor object
    cursor_obj = db.cursor()

    for incident in incidents:
        try:
            cursor_obj.execute("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)",
                       (incident['incident_time'], incident['incident_number'],
                        incident['incident_location'], incident['nature'], incident['incident_ori']))
        except:
            print('error in insertion')
    return len(incidents)
def status(db):
    op=db.execute("""SELECT nature || '|' || COUNT(*) AS row
    FROM incidents
    GROUP BY nature
    ORDER BY COUNT(*) DESC, nature ASC;

    """).fetchall()
    
    natures=""
    none=None
    # formatted_output = '\n'.join(row[0] for row in op)
    regex = re.compile(r'^None\|.*$', re.MULTILINE)
    for o in op:
        if(re.match(regex, o[0])):
            none=str(o[0])
            none=none.replace("None","")
            natures+=none+"\n"
        else:
            natures=natures+str(o[0])+"\n"
    # if none!=None:
    #     natures=natures+none.replace("None"," ")
    # if(none!=None):
    #     print(none)
    print(natures)
def deletedb(db):
    conn=db.cursor()
    conn.execute("DROP incidents")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)

