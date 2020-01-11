import requests
import sys
from bs4 import BeautifulSoup
from .logger import Logger
from .cpubenchmark import cpubenchmark_scraper_single, cpubenchmark_scraper_mega

logger = Logger("videocardbenchmark_sraper")

class single_gpu:
    def __init__(self, id=None, gpu_name=None, gpu_mark=None, gpu_rank=None, gpu_value=None, gpu_price=None):
        self._url = None
        self.id = id
        self._gpu_name = gpu_name
        self._gpu_mark = gpu_mark
        self._gpu_rank = gpu_rank
        self._gpu_value = gpu_value
        self._gpu_price = gpu_price

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if type(value) == str:
            value = value.replace("gpu", "")
        self._id = value
        self._url = "https://www.videocardbenchmark.net/gpu.php?id=%s" % str(value)

    def __repr__(self):
        return str(self.__dict__())

    def __dict__(self):
         return {"id": self.id, "url": self._url, "gpu_name": self._gpu_name,
                "gpu_mark": self._gpu_mark,  "gpu_rank": self._gpu_rank,
                "gpu_price": self._gpu_price, "gpu_value": self._gpu_value}

class mega_gpu:
    def __init__(self, id=None, gpu_name=None, gpu_price=None, gpu_mark=None, gpu_value=None, g2d_mark=None,
                    tdp=None, power_perf=None, test_date=None, category=None, bus_interface=None,
                    max_memory=None, core_clock=None, mem_clock=None, rank=None, samples=None):
        self._url = None
        self.id = id
        self._gpu_name = gpu_name
        self._gpu_price = gpu_price
        self._gpu_mark = gpu_mark
        self._gpu_value = gpu_value
        self._g2d_mark = g2d_mark
        self._tdp = tdp
        self._power_perf = power_perf
        self._test_date = test_date
        self._category = category
        self._bus_interface = bus_interface
        self._max_memory = max_memory
        self._core_clock = core_clock
        self._mem_clock = mem_clock
        self._rank = rank
        self._samples = samples

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if type(value) == str:
            value = value.replace("gpu", "")
        self._id = value
        self._url = "https://www.videocardbenchmark.net/gpu.php?id=%s" % str(value)

    def __repr__(self):
        return str(self.__dict__())

    def __dict__(self):
        return {"id": self.id, "url": self._url, "gpu_name": self._gpu_name,
                "gpu_price": self._gpu_price, "gpu_mark": self._gpu_mark,
                "gpu_value": self._gpu_value, "g2d_mark": self._g2d_mark,
                "tdp": self._tdp, "power_perf": self._power_perf,
                "test_date": self._test_date, "category": self._category,
                "bus_interface": self._bus_interface, "max_memory": self._max_memory,
                "core_clock": self._core_clock, "mem_clock": self._mem_clock,
                "rank": self._rank, "samples": self._samples}


class videocardbenchmark_scraper_single(cpubenchmark_scraper_single):
    def __init__(self, url="https://www.videocardbenchmark.net/gpu_list.php"):
        super().__init__(url=url)

    def refresh_gpus(self, raw_rows=None, headers=None):
        if raw_rows is None:
            raw_rows = self._raw_rows
        if headers is None:
            headers = self._headers
        _gpus = []
        for idx, row in enumerate(raw_rows):
            _cols = row.find_all('td')
            if len(_cols) < 5:
                    logger.warning("Not enough rows for GPU: %i" % idx)
            else:
                _id = row.get('id')
                if _id is None:
                    logger.warning("%s: unable to find GPU id, the url returned will most likely be wrong.")
                _gpus.append(single_gpu(id=_id, gpu_name=_cols[0].text, gpu_mark=_cols[1].text, gpu_rank=_cols[2].text,
                                        gpu_value=_cols[3].text, gpu_price=_cols[4].text))

        return _gpus

    def refresh_all(self):
        self._source = self.refresh_request()
        self._soup = self.refresh_soup()
        self._table = self.refresh_table()
        self._headers = self.refresh_headers()
        self._raw_rows = self.refresh_raw_rows()
        self._gpus = self.refresh_gpus()


class videocardbenchmark_scraper_mega(cpubenchmark_scraper_mega):
    def __init__(self, url='https://www.videocardbenchmark.net/GPU_mega_page.html'):
        super().__init__(url=url)

    def refresh_gpus(self, raw_rows=None, headers=None):
        if raw_rows is None:
            raw_rows = self._raw_rows
        if headers is None:
            headers = self._headers
        _gpus = []
        for idx, row in enumerate(raw_rows):
            _cols = row[0].find_all('td')
            _temp_gpu = {}
            print(len(_cols))
            if len(_cols) < 9:
                    logger.warning("Not enough rows for GPU: %i" % idx)
            else:
                _id = row[0].get('id')
                if _id is None:
                    logger.warning("%s: unable to find GPU id, the url returned will most likely be wrong.")
                _temp_gpu = dict(id=_id, gpu_name=_cols[0].text, gpu_price=_cols[1].text, gpu_mark=_cols[2].text,
                                        gpu_value=_cols[3].text, g2d_mark=_cols[4].text, tdp=_cols[5].text,
                                        power_perf=_cols[6].text, test_date=_cols[7].text, category=_cols[8].text)
            _cols2 = row[1].find_all('div')
            print(len(_cols2))
            if len(_cols2) < 6:
                logger.warning("Not enough MEGA rows for CPU: %i" % idx)
            else:
                _temp_gpu.update({"bus_interface": _cols2[0].text.replace("Bus Interface: ", ""),
                                "max_memory": _cols2[1].text.replace("Max Memory: ", ""), 
                                "core_clock": _cols2[2].text.replace("Core Clock: ", ""),
                                "mem_clock": _cols2[3].text.replace("Mem Clock: ", ""),
                                "rank": _cols2[4].text.replace("Rank: ", ""),
                                "samples": _cols2[5].text.replace("Samples: ", "")})
            _gpus.append(mega_gpu(**_temp_gpu))

        return _gpus

    def refresh_all(self):
        self._source = self.refresh_request()
        self._soup = self.refresh_soup()
        self._table = self.refresh_table()
        self._headers = self.refresh_headers()
        self._raw_rows = self.refresh_raw_rows()
        self._gpus = self.refresh_gpus()