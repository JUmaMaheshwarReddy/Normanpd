# CS5239sp22-Project0

## Author
**Jangalapalli Uma Maheshwar Reddy**

Author Email : umamaheshwarreddy.jangalapalli@ou.edu

---
Norman Police Department, Daily Incident Summary
===

![alt_text](https://www.normanok.gov/sites/default/files/styles/logo/public/images/2022-02/Badge.JPG?itok=uYhj6VWe)

# About

The Norman, Oklahoma police department regularly reports cases.
The website contains three types of summaries arrests,
incidents and case summaries.
The main goal of our project is to extract the data information
from a scrapped file which is a PDF file in the 
[Oklahoma Police Department](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports).
In this project we are only considering daily incidents and 
python is used to accomplish the project. The steps involved are
- Downloaded the data from the link.
- The data is extracted.
- Created the sqlite3 database to store the data.
- The empty spaces are replaced by value ` N/A `.
- Insert the data into the table ` incidents ` in database named `normanpd.db`.
- display the total types of nature(reason for arrest) and
count(number of times it appeared) which is seperated by a pipe '` | `'.
---
## Packages and libraries Required

- urllib.request
- re
- ssl
- tempfile
- PyPDF2
- sqlite3
- argparse
---

## Structure
```
cs5293sp22-project0/
├── COLLABORATORS
├── docs
├── LICENSE
├── requirements.txt
├── project0
│   ├── main.py
│   └── project0.py
├── README.md
├── normanpd.db
├── setup.cfg
├── setup.py
└── tests
    ├── test_download.py
    └── test_fields.py
```
---

## Assumptions
After analyzing multiple incident reports provided by the
Norman police department,
for this project I assumed that the fields are only 5 
and also assuming that empty spaces in the pdf
only occur in location and nature columns.

Other assumption is case number is always numeric and nature is always alphabetic.

Assuming that every pdf has cloumn names and first page has heading `"NORMAN POLICE DEPARTMENT", "Daily Incident Summary (Public)"`.

Assuming every row has date with time in the same(MM/DD/YYYY HOURS:MINS) format and every pdf has date at the end.

structure is in the form of :
```
CREATE TABLE IF NOT EXISTS incidents(
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
); 
```
---

# Description
To implement this project there are two main files:

**1. main.py**

**2. project0.py**

To test the package we have incidents.py,fields.py

### main .py

This file is invoked to process the data and output the results.

The main function has methods that are imported from **`project0.py`**.

- Method **`project0.fetchincidents(url)`** is used to fetch the data from url passed.
- Method **`project0.extractincidnets(incdient_data)`** is used to collect the data obtained from the website and store it.
- Method **`project0.createdb()`** is used to create the database and table.
- Method **`project0.populatedb(db,incidents)`** is used to insert the data into database.
- Method **`project0.statusdb(db)`** is used to display the data from the database that is required to be shown.

---
### project0.py

This package is used by `main.py` to call all the methods and fetch results from data base.

***fetchincidnents(url)***

This method takes input parameter as URL and it reads the data from the given URL.
This is achieved by the urllib.request package.
This function returns the data that is fetched and read from URL.

---
***extractincidents(data)***

This method takes the input parameter as data that is fetched from URL and 
parse it and store it into a list.

In this method I have used tempfile which allows to create temporary file
to store the data. The data is written to the variable created.

In this method I have also used PyPDF2 to read the data that is fetched and stored in temporary file.
I will store the count of the page that is in the pdf which i can use as length of loop.
A list is created to store the data.


To handle the line by line data I'm splitting the data into each row
using date regex by adding a "^" at the starting of date 
and # at end of date for each row first column. 
`temp = "^" + i + "#"`

I'm also adding @ for each record of second column for 
checking the length while inserting in database(for other method purpose).
`temp = r2 + "@"`

To search the pattern of regex we use :

`res = pattern.findall(pdfReader.getPage(eachpage).extractText())`

**Date and time regex, number regex as per PDF**
```
        mon = '([1-9]|1[0-2])'
        date = '([1-9]|1[0-9]|2[0-9]|3[0-1])'
        year = '(201[0-9]|202[0-9])'
        hourReg = '( [0-9]| [1][0-9]| 2[0-3])'
        minReg = '(:[0-5][0-9])'

        pattern = re.compile(mon + '/' + date + '/' + year + hourReg + minReg)
        number = re.compile(r'[0-9]*-[0-9]*')
```

After changing the column 1 and column 2 it is appended to the list.
The data is split based on date/time.

Now each incident is extracted now its attributes are seperated by `','` which was replaced instead `' \n'`.

```
final.append(page.replace(' \n',' ').replace('\n',',').strip(',').split('^'))
```

It is created as the list of lists.(each page is a list and page itself is a list)

While extracting attributes of Incidents, I have noticed some incidents more than 5 attributes. 
In page one, the additional attributes were title, subtitle and headings of columns. 
In last page there is a date of generation at end.

page one additional attributes are replaced with empty space.

```
page = pdfReader.getPage(eachpage).extractText().replace("NORMAN POLICE DEPARTMENT",'').replace("Daily Incident Summary (Public)",'')
```

headings of columns and Last page attribute are deleted after collecting it into list.

This function returns a list of list.

---
***createdb()***

This method takes no parameter and it is used to create a database named `'normanpd.db'`
and table named `'incidents'` in that database. 
If the database has already exists table 'incidents' created it will not create again. 
This method returns the database name.

Below is the code for creating table:
```
CREATE TABLE IF NOT EXISTS incidents(
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
); 
```
---
***populatedb(db,incidents)***

This method takes database name and 
incidents list(returned from extractincidents) as parameters
and inserts the data into database `normanpd.db` table `incidents`.
Every time the code is run the records in incidents are deleted and new records are inserted.

To insert the data into table we use:

```
cur.execute("insert into incidents values (?,?,?,?,?)"
```

In this method while inserting into database
im checking length of each row. I have taken max length 6,5,4,3,2,1.

Here, temp is a list which has each row. 
- so, temp[1] is first column(date/time),
- temp[2] is second column(Incident number),
- temp[3] is third column(address)
- temp[4] is fourth column(nature)
- temp[5] is fifth column(Incident ORI).

Also im removing the `'#'` symbol added to date at the end and `'@'` symbol added to incident number at end for each row. 

Assuming every row has date/time for compulsory. column 2 is always ended with `'@'`.
column 3,5 is alpha-numeric and column 5 is alphabetic. 

***For length == 6***

Assuming if length is 6 the address is split into two parts 
so im appending the temp[2] and temp[3].

```
(temp[0][:-1], temp[1][:-1], temp[2]+temp[3], temp[4],temp[5]))
```

***For length == 5***

Every record is inserted as it is as we have 5 columns to insert.

```
(temp[0], temp[1], temp[2], temp[3], temp[4]))
```

***For length == 4***

Assuming date column is not missing in any row.
If 2nd column is not ending with @ then it is replaced by `'N/A'`.
If the 3rd column is not alpha numeric then it is replaced by `'N/A'`.
If the 4th column is not alpha then it is replaced by `'N/A'`.
If the 5th column is not alpha numeric then it is replaced by `'N/A'`.

```
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
```

```Similarly for length 3,2,1 we replace the missing values with N/A.```

---
***statusdb(db)***

This method takes the database name as input parameter. 
It is used to fetch the summary of incidents which is stored in the database.

In this project we want the nature type 
and its count(times it appeared) separated by `'|'`.
It is displayed in decreasing order of count 
and same count of natures should be arranged in alphabetic order `'A-z'`.
It returns a stirng appended with all natures.


---
### Output:

```
Alarm | 23
Welfare Check | 20
N/A | 14
Sick Person | 13
Transfer/Interfacility | 13
MVA With Injuries | 12
```
---
***How to Run this code:***

To run this code you need to pass the command line as follows:

python project0/main.py --incidents "url"

```
python project0/main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"
```
---

### Test cases
***test***

The directory tests has two .py files(packages) with methods defined in them. 
These are used for unit testing the methods defined in the package **project0.py**.


***test/test_download.py/test_fetchincidents()***

This method is used to test method **fetchincidents(url)** in project0.py. 
In this, verifying if the object returned by 
**project0.fetchincidents(url)** when it is called is not None or not.

```
url_link = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"

def test_fectincidents():
    assert project0.fetchincidents(url_link) is not None
```

***test/test_fields***

***test_extractincidents()***

This method is used to test the method **extractincidents(incident_data)** in project0.py.
In this, verifying if the object returned is whether list or not and
its length is greater than 0 which means list is not empty.

```
    assert type(data_stored) == type([])
    assert len(data_stored) > 0
```

***test_createdb()***

This method is used to test method **createdb()** in project0.py.
In this, verifying if the database is created or not.

***test_populatedb()***

This method is used to test method **populatedb(db,incidents)** in project0.py.
In this, verifying if the all records are inserted into incidents table or not.
By querying the table a random result is given.

```
    cur.execute("SELECT * FROM incidents ORDER BY RANDOM() LIMIT 1")

    results = cur.fetchall()
    assert results is not None
```

***test_statusdb()***

This method is used to test method **statusdb(db)** in project0.py.
In this, Verifying if the data displayed is a stirng or not.

```
assert type(randominfo)== type("")
```

---
# External Resources
```
https://pythonhosted.org/PyPDF2/PdfFileReader.html
https://stackoverflow.com/questions/2520633/what-is-the-mm-dd-yyyy-regular-expression-and-how-do-i-use-it-in-php
https://pynative.com/python-regex-compile/
https://docs.python.org/3.8/library/sqlite3.html
https://stackoverflow.com/questions/8840303/urllib2-http-error-400-bad-request
https://www.programcreek.com/python/example/83039/ssl._create_unverified_context
https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports
https://sqlitebrowser.org/
```
---
### Bugs
```
The title, subtitle should be named as given in code.
There should be headings otherwise a row may get deleted.
There should be date at the end of the file.
The date column should be in same format for regex to work.
To clean the data to get desired output, I hardcoded some cases, So the code can handle only those conditions.
```
---
### Clone git hub and push code from linux
1. Create a git repository with name cs5293sp22-project0.
2. git clone "url".
3. create directory project0 and cd into directory.
4. create .py files named as main.py and project0.py.
**`vim main.py`**
5. similarly create tests files.
6. add file to git by git add file name and git commit.

**`git add main.py`**

**`git commit -m "comment"`**

**`git push origin main`**
7. Use your git hub username and key token as password.

---
### Directions to install and use packages

1. cd Create a directory and then cd into directory.
**`mkdir Text_project0 && cd Text_project0`**
2. Download the project from Github.
3. cd into project directory `cs5293sp22-project0`.
4. Install pipenv to create virtual environment and install python3.
**pip install pipenv**
5. install dependencies listed in **requirements.txt**.
**`pipenv install -r requirements.txt`**
6. After installing dependencies successfully run the unit tests.
**`pipenv run pytest`**
7. After running the unit tests you can run the above mentioned how to run code changing the URL.
---

