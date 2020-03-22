import requests
import sys
from bs4 import BeautifulSoup
from .logger import Logger
from .cpubenchmark import cpubenchmark_scraper_single, cpubenchmark_scraper_mega

logger = Logger("harddrivebenchmark_sraper")

class single_hdd:
    def __init__(
        self,
        id=None,
        hdd_name=None,
        hdd_size=None,
        hdd_mark=None,
        hdd_rank=None,
        hdd_value=None,
        hdd_price=None
    ):
        self._url = None
        self.id = id
        self._hdd_name = hdd_name
        self._hdd_size = hdd_size
        self._hdd_mark = hdd_mark
        self._hdd_rank = hdd_rank
        self._hdd_value = hdd_value
        self._hdd_price = hdd_price
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if type(value) == str:
            value = value.replace("gpu", "")
        self._id = value
        self._url = "https://www.harddrivebenchmark.net/hdd.php?id=%s" % str(value)

    def __repr__(self):
        return str(self.__dict__())

    def __dict__(self):
        return {
            "id": self.id,
            "url": self._url,
            "hdd_name": self._hdd_name,
            "hdd_size": self._hdd_size,
            "hdd_mark": self._hdd_mark,
            "hdd_rank": self._hdd_rank,
            "hdd_value": self._hdd_value,
            "hdd_price": self._hdd_price
        }


class mega_hdd:
    def __init__(
        self,
        id=None,
        hdd_name=None,
        hdd_size=None,
        hdd_mark=None,
        hdd_samples=None,
        hdd_rank=None,
        hdd_price=None,
        hdd_value=None,
        test_date=None,
        hdd_type=None
    ):
        self._url = None
        self.id = id
        self._hdd_name = hdd_name
        self._hdd_size = hdd_size
        self._hdd_mark = hdd_mark
        self._hdd_samples = hdd_samples
        self._hdd_rank = hdd_rank
        self._hdd_price = hdd_price
        self._hdd_value = hdd_value
        self._test_date = test_date
        self._hdd_type = hdd_type

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if type(value) == str:
            value = value.replace("gpu", "")
        self._id = value
        self._url = "https://www.harddrivebenchmark.net/hdd.php?&id=%s" % str(value)

    def __repr__(self):
        return str(self.__dict__())

    def __dict__(self):
        return {
            "id": self.id,
            "url": self._url,
            "hdd_name": self._hdd_name,
            "hdd_size": self._hdd_size,
            "hdd_mark": self._hdd_mark,
            "hdd_samples": self._hdd_samples,
            "hdd_rank": self._hdd_rank,
            "hdd_price": self._hdd_price,
            "hdd_value": self._hdd_value,
            "test_date": self._test_date,
            "hdd_type": self._hdd_type
        }


class harddrivebenchmark_scraper_single(cpubenchmark_scraper_single):
    def __init__(self, url="https://www.harddrivebenchmark.net/hdd_list.php"):
        super().__init__(url=url)

    def refresh_hdds(self, raw_rows=None, headers=None):
        if raw_rows is None:
            raw_rows = self._raw_rows
        if headers is None:
            headers = self._headers
        _hdds = []
        for idx, row in enumerate(raw_rows):
            _cols = row.find_all("td")
            if len(_cols) < 5:
                logger.warning("Not enough columns for HDD: %i" % idx)
                raise Exception("Not enough columns in table for extraction")
            else:
                _id = _cols[0].find('a').attrs['href'].split('id=')[-1]
                if _id is None:
                    logger.warning(
                        "%s: unable to find HDD id, the url returned will most likely be wrong."
                    )
                _hdds.append(
                    single_hdd(
                        id=_id,
                        hdd_name=_cols[0].text,
                        hdd_size=_cols[1].text,
                        hdd_mark=_cols[2].text,
                        hdd_rank=_cols[3].text,
                        hdd_value=_cols[4].text,
                        hdd_price=_cols[5].text
                    )
                )

        return _hdds

    def refresh_all(self):
        self._source = self.refresh_request()
        self._soup = self.refresh_soup()
        self._table = self.refresh_table()
        self._headers = self.refresh_headers()
        self._raw_rows = self.refresh_raw_rows()
        self._hdds = self.refresh_hdds()


class harddrivebenchmark_scraper_mega(cpubenchmark_scraper_mega):
    def __init__(self, url="https://www.harddrivebenchmark.net/hdd-mega-page.html"):
        super().__init__(url=url)

    def refresh_hdds(self, raw_rows=None, headers=None):
        if raw_rows is None:
            raw_rows = self._raw_rows
        if headers is None:
            headers = self._headers
        _hdds = []
        for idx, row in enumerate(raw_rows):
            _cols = row[0].find_all("td")
            if len(_cols) < 9:
                logger.warning("Not enough columns for GPU: %i" % idx)
                raise Exception("Not enough columns in table for extraction")
            else:
                _id = _cols[0].find('a').attrs['href'].split('id=')[-1]
                if _id is None:
                    logger.warning(
                        "%s: unable to find GPU id, the url returned will most likely be wrong."
                    )
                _hdds.append(mega_hdd(
                    id=_id,
                    hdd_name=_cols[0].text,
                    hdd_size=_cols[1].text,
                    hdd_mark=_cols[2].text,
                    hdd_samples=_cols[3].text,
                    hdd_rank=_cols[4].text,
                    hdd_price=_cols[5].text,
                    hdd_value=_cols[6].text,
                    test_date=_cols[7].text,
                    hdd_type=_cols[8].text
                ))

        return _hdds

    def refresh_all(self):
        self._source = self.refresh_request()
        self._soup = self.refresh_soup()
        self._table = self.refresh_table()
        self._headers = self.refresh_headers()
        self._raw_rows = self.refresh_raw_rows()
        self._hdds = self.refresh_hdds()
