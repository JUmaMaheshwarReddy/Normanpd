import re
import urllib.request
import ssl
import tempfile
import PyPDF2

ssl._create_default_https_context = ssl._create_unverified_context

# def fetchincidents():

url = ("https://www.normanok.gov/sites/default/files/documents/2022-01/2022-01-01_daily_incident_summary.pdf")
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
data = urllib.request.urlopen(
    urllib.request.Request(
        url, headers=headers)).read()
# return data


# def extractincidents(data):
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
    print(eachpage)
    date_regex = '(0[1-9]|1[0-2])[- /.](0[1-9]|1[0-9]|2[0-9]|3[0-1])[- /.](201[0-9]|202[0-9])/d/d'
    mon = '([1-9]|1[0-2])'
    date = '([1-9]|1[0-9]|2[0-9]|3[0-1])'
    year = '(201[0-9]|202[0-9])'
    hourReg = '( [0-9]| [1][0-9]| 2[0-3])'
    minReg = '(:[0-5][0-9])'

    pattern = re.compile(mon + '/' + date + '/' + year + hourReg + minReg)

    # pattern =
    # re.search(r'(0[1-9]|1[0-2])[/](0[1-9]|1[0-9]|2[0-9]|3[0-1])[/](201[0-9]|202[0-9])')

    res = pattern.findall(pdfReader.getPage(eachpage).extractText())
    out = set()
    for i in res:
        i = '/'.join(i)
        i = i.replace('/ ', ' ')
        i = i.replace('/:', ':')
        temp = ";" + i
        if temp not in out:
            out.add(
                temp)
            page = page.replace(i, temp)
            # print(page6)
            final.append(
                page.replace(
                    ' \n',
                    ' ').replace(
                    '\n',
                    ',').strip(',').split(';'))

    for h in final:
                h.pop(
                    0)
                print(
                    h)
                # print(final[0])

                print(
                    final)
                final[-1].pop()

                # for pagenum in range(1, pagecount):
                #   p = pdfReader.getPage(1).extractText()

                # def createdb():
 import sqlite3
 connection = sqlite3.connect(r'normanpd.db')
                cur = connection.cursor()
                table = """ CREATE TABLE IF NOT EXISTS incidents(incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT)"""

                cur.execute(
                    table)
                cur.execute(
                    """DELETE FROM incidents""")

                for item in range(
                        0, len(final)):
                    for record in final[item]:
                        print(len(record.strip(',').split(
                            ',')), record.strip(','))
                        if(len(record.strip(',').split(',')) == 5):
                            temp = record.strip(
                                ',').split(',')
                            cur.execute("insert into incidents values (?,?,?,?,?)",
                                        (temp[0], temp[1], temp[2], temp[3], temp[4]))

                            connection.commit()

                            # def
                            # populatedb(db,incidents):
                            for record in cur.execute(
                                    "SELECT * FROM incidents"):
                                print(
                                    record)

                                # return
                                # ''

                                # def
                                # status
                                # of
                                # db
                                for record in cur.execute(
                                        "SELECT nature,COUNT(nature) FROM incidents GROUP BY nature ORDER BY COUNT(nature) DESC, nature ASC"):
                                    # record.replace(',','|').slipt('\n')
                                    print(record)