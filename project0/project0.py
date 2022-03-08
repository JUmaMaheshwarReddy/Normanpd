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

    # url =
    # ("https://www.normanok.gov/sites/default/files/documents/2022-01/2022-01-01_daily_incident_summary.pdf")
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
        number = re.compile(r'[0-9]*-[0-9]*')

        # number = re.compile(r'[0-9]{4}-[0-9]{9}')
        # number = re.compile('[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
        # number = re.compile(r'\d\d\d\d-\d\d\d\d\d\d\d\d')
        # address = re.compile()
        # address = re.compile(r'[a-zA-Z0-9\s]*')
        # nature = re.compile(r'\sA-Za-z0-9\/*')

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
                out.add(temp)
                page = page.replace(i, temp)
                # print(page6)

        res2 = number.findall(pdfReader.getPage(eachpage).extractText())
        # print(res2)
        out = set()
        for r2 in res2:
            temp = r2 + "@"
            if temp not in out:
                out.add(temp)
                page = page.replace(r2, temp)
                # print(page)
        final.append(
            page.replace(
                ' \n',
                ' ').replace(
                '\n',
                ',').strip(',').split(';'))
        # res3 = address.findall(pdfReader.getPage(eachpage).extractText())
        # print(res3)
    # print(final[0])

    for h in final:
        h.pop(0)
        # print(h)
    # print(final[0])

    # print(final)
    final[-1].pop()

    # for item in range(0,len(final)):
    #     for record in final[item]:
    #         recordlen = len(record.strip(',').split(','))
    #         #print(recordlen)
    #         #print(len(record.strip(',').split(',')),record.strip(','))
    #         temp = record.strip(',').split(',')
    #
    #         if (recordlen == 6):
    #             print(temp[0][:-1], temp[1][:-1], temp[2]+temp[3], temp[4],temp[5])
    #         if(recordlen == 5):
    #             print(temp[0][:-1], temp[1][:-1], temp[2], temp[3], temp[4])
    #
    #
    #         if(recordlen == 4):
    #             if(temp[1][-1] != "@"):
    #                 print(temp[0][:-1], "N/A" , temp[1], temp[2], temp[3])
    #             elif(not temp[2].isalnum()):
    #                 print(temp[0][:-1], temp[1][:-1], "N/A", temp[2], temp[3])
    #             elif(not temp[3].isalpha()):
    #                 print(temp[0][:-1], temp[1][:-1], temp[2], "N/A", temp[3])
    #             else:
    #                 print(temp[0][:-1], temp[1][:-1], temp[2], temp[3], "N/A")
    #
    #         if(recordlen == 3):
    #             #print(temp[1][-1])
    #             #print(temp[2])
    #             #print(temp[2].isalnum())
    #
    #             if((temp[1][-1] == "@") and (temp[2].isalnum())):
    #                 print(temp[0][:-1],temp[1][:-1] , "N/A", "N/A", temp[2])
    #             if((temp[1][-1] != "@") and (temp[2].isalnum()) and (temp[1].isalnum())):
    #                 print(temp[0][:-1], "N/A",temp[1],"N/A", temp[2])
    #
    #         if(recordlen == 2):
    #             if((not temp[2].isalnum()) and (not temp[3].isalpha()) and (not temp[4].isalnum())):
    #                 print(temp[0][:-1], temp[1][:-1], "N/A", "N/A", "N/A")
    #             elif((temp[1][-1] != "@") and (not temp[3].isalpha()) and (not temp[4].isalnum())):
    #                 print(temp[0][:-1], "N/A",temp[1],"N/A", "N/A")
    #             elif((temp[1][-1] != "@") and (not temp[2].isalnum()) and (not temp[4].isalnum())):
    #                 print(temp[0][:-1], "N/A","N/A",temp[1], "N/A")
    #             elif((temp[1][-1] != "@") and (not temp[2].isalnum()) and (not temp[3].isalpha())):
    #                 print(temp[0][:-1], "N/A", "N/A", "N/A",temp[1])
    #
    #         if(recordlen == 1):
    #             print(temp[0][:-1], "N/A", "N/A", "N/A", "N/A")

    return final


def createdb():
    connection = sqlite3.connect(r'normanpd.db')
    cur = connection.cursor()
    table = """ CREATE TABLE IF NOT EXISTS incidents(incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT)"""

    cur.execute(table)
    # cur.execute("""DELETE FROM incidents""")
    return 'normanpd.db'


def populatedb(db, final):
    # import sqlite3
    connection = sqlite3.connect(r'normanpd.db')
    cur = connection.cursor()
    cur.execute("""DELETE FROM incidents""")
    for item in range(0, len(final)):
        for record in final[item]:
            recordlen = len(record.strip(',').split(','))
            # print(recordlen)
            # print(len(record.strip(',').split(',')),record.strip(','))
            temp = record.strip(',').split(',')
            if (recordlen == 6):
                cur.execute("insert into incidents values (?,?,?,?,?)",
                            (temp[0][:-1], temp[1][:-1], temp[2] + temp[3], temp[4], temp[5]))

            if(recordlen == 5):
                cur.execute("insert into incidents values (?,?,?,?,?)",
                            (temp[0], temp[1], temp[2], temp[3], temp[4]))

            if (recordlen == 4):
                if (temp[1][-1] != "@"):
                    cur.execute("insert into incidents values (?,?,?,?,?)",
                                (temp[0][:-1], "N/A", temp[1], temp[2], temp[3]))
                elif (not temp[2].isalnum()):
                    cur.execute("insert into incidents values (?,?,?,?,?)",
                                (temp[0][:-1], temp[1][:-1], "N/A", temp[2], temp[3]))
                elif (not temp[3].isalpha()):
                    cur.execute("insert into incidents values (?,?,?,?,?)",
                                (temp[0][:-1], temp[1][:-1], temp[2], "N/A", temp[3]))
                else:
                    cur.execute("insert into incidents values (?,?,?,?,?)",
                                (temp[0][:-1], temp[1][:-1], temp[2], temp[3], "N/A"))

            if(recordlen == 3):
                # print(temp[1][-1])
                # print(temp[2])
                # print(temp[2].isalnum())

                if((temp[1][-1] == "@") and (temp[2].isalnum())):
                    cur.execute("insert into incidents values (?,?,?,?,?)",
                                (temp[0][:-1], temp[1][:-1], "N/A", "N/A", temp[2]))
                if((temp[1][-1] != "@") and (temp[2].isalnum()) and (temp[1].isalnum())):
                    cur.execute("insert into incidents values (?,?,?,?,?)",
                                (temp[0][:-1], "N/A", temp[1], "N/A", temp[2]))

            if (recordlen == 2):
                if ((not temp[2].isalnum()) and (
                        not temp[3].isalpha()) and (not temp[4].isalnum())):
                    cur.execute("insert into incidents values (?,?,?,?,?)",
                                (temp[0][:-1], temp[1][:-1], "N/A", "N/A", "N/A"))
                elif ((temp[1][-1] != "@") and (not temp[3].isalpha()) and (not temp[4].isalnum())):
                    cur.execute("insert into incidents values (?,?,?,?,?)",
                                (temp[0][:-1], "N/A", temp[1], "N/A", "N/A"))
                elif ((temp[1][-1] != "@") and (not temp[2].isalnum()) and (not temp[4].isalnum())):
                    cur.execute("insert into incidents values (?,?,?,?,?)",
                                (temp[0][:-1], "N/A", "N/A", temp[1], "N/A"))
                elif ((temp[1][-1] != "@") and (not temp[2].isalnum()) and (not temp[3].isalpha())):
                    cur.execute("insert into incidents values (?,?,?,?,?)",
                                (temp[0][:-1], "N/A", "N/A", "N/A", temp[1]))

            if (recordlen == 1):
                cur.execute("insert into incidents values (?,?,?,?,?)",
                            (temp[0][:-1], "N/A", "N/A", "N/A", "N/A"))
    connection.commit()

    # for record in cur.execute("SELECT COUNT(*) FROM incidents"):
    # print(record)


def status(db):
    import sqlite3
    connection = sqlite3.connect(r'normanpd.db')
    cur = connection.cursor()
    f = ""
    for record in cur.execute(
            "SELECT nature,COUNT(nature) FROM incidents GROUP BY nature ORDER BY COUNT(nature) DESC, nature ASC"):
        # record.replace(',','|').slipt('\n')
        print("{}{}{}".format(record[0], ' | ', record[1]))
        f = f + record[0]
    # print(f)

    return f
