import requests
import sys
from bs4 import BeautifulSoup
from itertools import zip_longest
from .logger import Logger

logger = Logger("cpubenchmark_sraper")



def grouper(iterable, n, fillvalue=None): # https://stackoverflow.com/a/434411/12633579
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

class single_cpu:
    def __init__(self, id=None, name=None, mark=None, rank=None, value=None, price=None):
        self._url = None
        self._id = id
        self.id = id
        self._name = name
        self._mark = mark
        self._rank = rank
        self._value = value
        self._price = price   

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if type(value) == str:
            value = value.replace("cpu", "")
        self._id = value
        self._url = "https://www.cpubenchmark.net/cpu.php?id=%s" % str(value)

    def __repr__(self):
        return str(self.__dict__())

    def __dict__(self):
        return {"id": self._id, "url": self._url, "name": self._name, "mark": self._mark,
                "rank": self._rank, "value": self._value, "price": self._price}

class mega_cpu:
    def __init__(self, id=None, cpu_name=None, cpu_price=None, cpu_mark=None, cpu_value=None, thread_mark=None, thread_value=None,
                        tdp=None, power_perf=None, test_date=None, socket=None, category=None, clock_speed=None,
                        turbo_speed=None, cores=None, rank=None, samples=None):
        self._url = None
        self._id = id
        self.id = id
        self._cpu_name = cpu_name
        self._cpu_price = cpu_price
        self._cpu_mark = cpu_mark
        self._cpu_value = cpu_value
        self._thread_mark = thread_mark
        self._thread_value = thread_value
        self._tdp = tdp
        self._power_perf = power_perf
        self._test_date = test_date
        self._socket = socket
        self._category = category
        self._clock_speed = clock_speed
        self._turbo_speed =turbo_speed
        self._cores = cores
        self._rank = rank
        self._samples = samples

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if type(value) == str:
            value = value.replace("cpu", "")
        self._id = value
        self._url = "https://www.cpubenchmark.net/cpu.php?id=%s" % str(value)

    def __repr__(self):
        return str(self.__dict__())

    def __dict__(self):
        return {"id": self.id, "url": self._url, "cpu_name": self._cpu_name, "cpu_price": self._cpu_price, "cpu_mark": self._cpu_mark,
                "cpu_value": self._cpu_value, "thread_mark": self._thread_mark, "thread_value": self._thread_value,
                "tdp": self._tdp, "power_perf": self._power_perf, "test_date": self._test_date, 
                "socket": self._socket, "category": self._category, "clock_speed": self._clock_speed,
                "turbo_speed": self._turbo_speed, "cores": self._cores, "rank": self._rank, "samples": self._samples}



class cpubenchmark_scraper_single:
    def __init__(self, url="https://www.cpubenchmark.net/cpu_list.php"):
        self._url = url
        logger.info("Set URL as %s" % url)
        self._source = None
        self._soup = None
        self._table = None
        self._headers = None
        self._raw_rows = None
        self._cpus = None

    def refresh_request(self, url=None):
        if url is None:
            url = self._url
        try:
            _source = requests.get(url).text
        except requests.exceptions.RequestException as e: 
            logger.critical("Requests failed to reach %s, error: %s" % (url, e))
            sys.exit(1)
        logger.info("Requests discovered the webpage successfully")
        return _source

    def refresh_soup(self, source=None, features="html.parser"):
        if source is None:
            source = self._source
        try:
            _soup = BeautifulSoup(source, features=features)
        except Exception as e:
            logger.critical("BS4 failed to create a BeautifulSoup instance, error: %s" % e)
            sys.exit(1)
        logger.info("BS4 successfully created a BeautifulSoup instance")
        return _soup

    def refresh_table(self, soup=None):
        if soup is None:
            soup = self._soup
        _table = self._soup.find('table', {'id': 'cputable'})
        if _table is None:
            logger.critical("BS4 was unable to find any table on this website by the id 'cputable'")
            sys.exit(1)
        else:
            logger.info("BS4 successfully discovered a table by the id 'cputable'")
        return _table

    def refresh_headers(self, table=None):
        if table is None:
            table = self._table
        try:
            _header_row = table.find('thead')
            _header_cols = _header_row.find_all('th')
            _header_cols_txt = [col.text for col in _header_cols]
        except AttributeError as e:
            logger.critical("BS4 was unable to find any headers on this table, error: %s" % e)
            sys.exit(1)
        logger.info("BS4 successfully discovered headers on this table: %s" % _header_cols_txt)
        return _header_cols

    def refresh_raw_rows(self, table=None):
        if table is None:
            table = self._table
        try:
            _cpu_body = table.find('tbody')
            _cpu_rows = _cpu_body.find_all('tr')
            if _cpu_rows is None:
                AttributeError("AttributeError: 'NoneType' object has no attribute 'find_all'")
        except AttributeError as e:
            logger.critical("BS4 was unable to find any rows on this table, error: %s" % e)
            sys.exit(1)
        logger.info("BS4 successfully discovered rows on this table")
        return _cpu_rows

    def refresh_cpus(self, raw_rows=None, headers=None):
        if raw_rows is None:
            raw_rows = self._raw_rows
        if headers is None:
            headers = self._headers
        _cpus = []
        for idx, row in enumerate(raw_rows):
            _cols = row.find_all('td')
            if len(_cols) < 5:
                    logger.warning("Not enough rows for CPU: %i" % idx)
            else:
                _id = row.get('id')
                if _id is None:
                    logger.warning("%s: unable to find CPU id, the url returned will most likely be wrong.")
                _cpus.append(single_cpu(id=_id, name=_cols[0].text, mark=_cols[1].text, rank=_cols[2].text,
                                value=_cols[3].text, price=_cols[4].text))

        return _cpus

    def refresh_all(self):
        self._source = self.refresh_request()
        self._soup = self.refresh_soup()
        self._table = self.refresh_table()
        self._headers = self.refresh_headers()
        self._raw_rows = self.refresh_raw_rows()
        self._cpus = self.refresh_cpus()

class cpubenchmark_scraper_mega(cpubenchmark_scraper_single):
    def __init__(self, url="https://www.cpubenchmark.net/CPU_mega_page.html"):
        super().__init__(url=url)
    
    def refresh_raw_rows(self, table=None):
        if table is None:
            table = self._table
        try:
            _cpu_body = table.find('tbody')
            _cpu_rows = _cpu_body.find_all('tr')
            if _cpu_rows is None:
                AttributeError("AttributeError: 'NoneType' object has no attribute 'find_all'")
            _cpu_rows = grouper(_cpu_rows, 2)
        except AttributeError as e:
            logger.critical("BS4 was unable to find any rows on this table, error: %s" % e)
            sys.exit(1)
        logger.info("BS4 successfully discovered rows on this table")
        return _cpu_rows
    
    def refresh_cpus(self, raw_rows=None, headers=None):
        if raw_rows is None:
            raw_rows = self._raw_rows
        if headers is None:
            headers = self._headers
        _cpus = []
        for idx, row in enumerate(raw_rows):
            _cols = row[0].find_all('td')
            _temp_cpu = {}
            if len(_cols) < 11:
                    logger.warning("Not enough rows for CPU: %i" % idx)
            else:
                _id = row[0].get('id')
                if _id is None:
                    logger.warning("%s: unable to find CPU id, the url returned will most likely be wrong.")
                _temp_cpu = dict(id=_id, cpu_name=_cols[0].text, cpu_price=_cols[1].text, cpu_mark=_cols[2].text, cpu_value=_cols[3].text,
                                         thread_mark=_cols[4].text, thread_value=_cols[5].text, tdp=_cols[6].text, power_perf=_cols[7].text,
                                         test_date=_cols[8].text, socket=_cols[9].text, category=_cols[10].text)
            _cols2 = row[1].find_all('div')
            if len(_cols2) < 5:
                logger.warning("Not enough MEGA rows for CPU: %i" % idx)
            else:
                _temp_cpu.update({"clock_speed": _cols2[0].text.replace("Clock Speed: ", ""), 
                                "turbo_speed": _cols2[1].text.replace("Turbo Speed: ", ""), 
                                "cores": _cols2[2].text.replace("No of Cores: ", ""), 
                                "rank": _cols2[3].text.replace("Rank: ", ""),
                                "samples": _cols2[4].text.replace("Samples: ", "")})
            _cpus.append(mega_cpu(**_temp_cpu))

        return _cpus