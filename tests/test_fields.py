import pytest
import sqlite3

from project0 import project0

url_link = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"


def test_extractincidents():
    links = project0.fetchincidents(url_link)
    data_stored = project0.extractincidents(links)

    assert data_stored is not None

    assert type(data_stored) == type([])

database = 'normanpd.db'

def test_createdb():
    dbname = project0.createdb()
    assert dbname == database

def test_populatedb():
    #dbname = project0.createdb()
    data = project0.fetchincidents(url_link)
    incidents = project0.extractincidents(data)
    sql = sqlite3.connect(database)
    cur = sql.cursor()
    cur.execute("SELECT * FROM incidents ORDER BY RANDOM() LIMIT 1")

    results = cur.fetchall()
    assert results is not None

def test_status():
    links = project0.fetchincidents(
                    url_link)
    data = project0.extractincidents(links)
    #database = project0.createdb()
    randominfo = project0.status(database)
    assert type(randominfo) == type("")
