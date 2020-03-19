from passmark_scraper import cpubenchmark
import bs4
from itertools import zip_longest
import unittest


scraper_single = cpubenchmark.cpubenchmark_scraper_single()
scraper_mega = cpubenchmark.cpubenchmark_scraper_mega()

class cpubenchmark_scraper_singleTest(unittest.TestCase):
    def setUp(self):
        self.scraper = scraper_single
    
    def test1_refresh_request(self):
        self.scraper._source = self.scraper.refresh_request()
        self.assertIs(type(self.scraper._source), str)

    def test2_refresh_soup(self):
        self.scraper._soup = self.scraper.refresh_soup()
        self.assertIs(type(self.scraper._soup), bs4.BeautifulSoup)

    def test3_refresh_table(self):
        self.scraper._table = self.scraper.refresh_table()
        self.assertIs(type(self.scraper._table), bs4.element.Tag)

    def test4_refresh_headers(self):
        self.scraper._headers = self.scraper.refresh_headers()
        self.assertIs(type(self.scraper._headers), bs4.element.ResultSet)

    def test5_refresh_raw_rows(self):
        self.scraper._raw_rows = self.scraper.refresh_raw_rows()
        self.assertIs(type(self.scraper._raw_rows), bs4.element.ResultSet)
    
    def test6_refresh_cpus(self):
        self.scraper._cpus = self.scraper.refresh_cpus()
        self.assertIs(type(self.scraper._cpus), list)
        
    def test7_refresh_all(self):
        self.scraper.refresh_all()
        self.assertIs(type(self.scraper._source), str)
        self.assertIs(type(self.scraper._soup), bs4.BeautifulSoup)
        self.assertIs(type(self.scraper._table), bs4.element.Tag)
        self.assertIs(type(self.scraper._headers), bs4.element.ResultSet)
        self.assertIs(type(self.scraper._raw_rows), bs4.element.ResultSet)
        self.assertIs(type(self.scraper._cpus), list)

class cpubenchmark_scraper_megaTest(cpubenchmark_scraper_singleTest):
    def setUp(self):
        self.scraper = scraper_mega

    def test5_refresh_raw_rows(self):
        self.scraper._raw_rows = self.scraper.refresh_raw_rows()
        self.assertIs(type(self.scraper._raw_rows), zip_longest)

    def test7_refresh_all(self):
        self.scraper.refresh_all()
        self.assertIs(type(self.scraper._source), str)
        self.assertIs(type(self.scraper._soup), bs4.BeautifulSoup)
        self.assertIs(type(self.scraper._table), bs4.element.Tag)
        self.assertIs(type(self.scraper._headers), bs4.element.ResultSet)
        self.assertIs(type(self.scraper._raw_rows), zip_longest)
        self.assertIs(type(self.scraper._cpus), list)



if __name__ == '__main__':
    unittest.main()