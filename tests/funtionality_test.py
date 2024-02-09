import requests
import pypdf
import pytest
import re
from urllib.request import urlretrieve


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

@pytest.mark.parametrize("pdf_url, expected_count",[
    ("https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-04_daily_incident_summary.pdf", 336),
    ("https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf", 328),
])
def test_extract_data_from_pdf(pdf_url, expected_count):
    result = extractincidents(pdf_url)
    assert len(result) == expected_count