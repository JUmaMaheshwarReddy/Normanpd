# CS5239sp22-Project0

## Author
**J Uma Maheshwar Reddy**

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

## Assumptions
After analyzing multiple incident reports provided by the
Norman police department,
for this project i assumed that the fields are only 5 
and also assuming that empty spaces in the pdf
only occur in location and nature columns.

Other assumption is case number is always numeric and nature is always alphabetic.

Assuming that the first page has heading `"NORMAN POLICE DEPARTMENT", "Daily Incident Summary (Public)"`.

Assuming every row has date with time in the same(MM/DD/YYYY HOURS:MINS) format in every pdf.

Assuming every pdf has date at the end.

structure is in the form of :
```
CREATE TABLE incidents(
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

### project0.py

This package is used by `main.py` to call all the methods and fetch results from data base.

***fetchincidnents(url)***

This method takes input parameter as URL and it reads the data from the given URL.
This is achieved by the urllib.request package.
This function returns the data that is fetched and read from URL.

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

`final.append(page.replace(' \n',' ').replace('\n',',').strip(',').split('^'))`

It is created as the list of lists.(each page is a list and page itself is a list)

While extracting attributes of Incidents, I have noticed some incidents more than 5 attributes. 
In page one, the additional attributes were title, subtitle. 
In last page there is a date of generation at end.

page one additional attributes are replaced with empty space.

`page = pdfReader.getPage(eachpage).extractText().replace("NORMAN POLICE DEPARTMENT",'').replace("Daily Incident Summary (Public)",'')`

Last page attribute is deleted after collecting it into list.

This function returns a list of list.

***createdb()***

This method takes no parameter and it is used to create a database named `'normanpd.db'`
and table named `'incidents'` in that database. This method returns the database name.

Below is the code for creating table:
```
CREATE TABLE incidents(
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
); 
```
