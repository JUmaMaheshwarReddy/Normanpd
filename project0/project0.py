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
