import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scrapper import WikiScrapper

@pytest.fixture
def scrapper():
    return WikiScrapper("")

@pytest.fixture
def local_file():
    return "tests/Team_Rocket.html"

def test_table(scrapper, local_file):
    scrapper.scrape(local_file=local_file)
    df = scrapper.get_table(1, first_headers=True)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    
def test_summary(scrapper, local_file):
    scrapper.scrape(local_file=local_file)
    summary = scrapper.get_summary()

    assert isinstance(summary, str)
    assert len(summary) == 238

def test_open_local_file_that_doesnt_exists(scrapper):
    with pytest.raises(FileNotFoundError):
        scrapper.scrape(local_file="maslo.html")

   