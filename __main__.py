from .logger import Logger
from .videocardbenchmark import videocardbenchmark_scraper_mega

if __name__ == "__main__":
    scraper = videocardbenchmark_scraper_mega()
    scraper.refresh_all()
    print(scraper._gpus)