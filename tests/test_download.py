import pytest

from project0 import project0

url_link = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-02_daily_incident_summary.pdf"

def test_fectincidents():
        assert project0.fetchincidents(url_link) is not None
