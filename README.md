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
[Oklahoma Police Department](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports)
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

The libraries can be installed using command ` 'pipenv install 'library_name' `.

---

## Assumptions
After analyzing multiple incident reports provided by the
Norman police department,
for this project i assumed that the fields are only 5 
and also assuming that empty spaces in the pdf
only occur in location and nature columns.
Other assumption is case number is always numeric and nature is always alphabetic.

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


