import re
import urllib.request
import ssl
import tempfile
import PyPDF2
import sqlite3


try:
    ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = ssl._create_unverified_context


def fetchincidents(url):

    #url = ("https://www.normanok.gov/sites/default/files/documents/2022-01/2022-01-01_daily_incident_summary.pdf")
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    data = urllib.request.urlopen(
        urllib.request.Request(
            url, headers=headers)).read()
    return data


def extractincidents(data):
    fp = tempfile.TemporaryFile()
    fp.write(data)
    fp.seek(0)

    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    pagecount = pdfReader.getNumPages()
    # print(pagecount)
    final = []

    # Get the first page
    for eachpage in range(pagecount):
        page = pdfReader.getPage(eachpage).extractText().replace(
            "NORMAN POLICE DEPARTMENT", '').replace(
            "Daily Incident Summary (Public)", '')
        # print(eachpage)
        date_regex = '(0[1-9]|1[0-2])[- /.](0[1-9]|1[0-9]|2[0-9]|3[0-1])[- /.](201[0-9]|202[0-9])/d/d'
        mon = '([1-9]|1[0-2])'
        date = '([1-9]|1[0-9]|2[0-9]|3[0-1])'
        year = '(201[0-9]|202[0-9])'
        hourReg = '( [0-9]| [1][0-9]| 2[0-3])'
        minReg = '(:[0-5][0-9])'

        pattern = re.compile(mon + '/' + date + '/' + year + hourReg + minReg)

    #pattern = re.search(r'(0[1-9]|1[0-2])[/](0[1-9]|1[0-9]|2[0-9]|3[0-1])[/](201[0-9]|202[0-9])')


