# -*- coding: utf-8 -*-
from passmark_scraper import harddrivebenchmark
import csv

def ex2csv_get_harddrivebenchmark_single():
    """
    Export the cpubenchmark single cpu system scrape to a csv file
    """
    scraper = harddrivebenchmark.harddrivebenchmark_scraper_single() # Initiliaze the harddrivebenchmark_scraper_single class
    scraper.refresh_all() # Refresh the web page, and scrape all of its data into scraper._hdds

    with open('harddrivebenchmark_single.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f) # Create new csv writer instance
        writer.writerow(["Drive Name", "Size", "Disk Rating (higher is better)", "Rank (lower is better)", "Drive Value (higher is better)"]) # Write the headings for the csv
        for hdd in scraper._hdds: # Iterate over all of the hdd_single classes
            writer.writerow([hdd._hdd_name, hdd._hdd_size, hdd._hdd_mark, hdd._hdd_rank, hdd._hdd_value, hdd._hdd_price]) # Write the row of the data

def ex2csv_get_harddrivebenchmark_mega():
    """
    Export the cpubenchmark mega cpu scrape to a csv file
    """
    scraper = harddrivebenchmark.harddrivebenchmark_scraper_mega() # Initiliaze the cpubenchmark_scraper_mega class
    scraper.refresh_all() # Refresh the web page, and scrape all of its data into scraper._cpus

    with open('harddrivebenchmark_mega.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f) # Create new csv writer instance
        writer.writerow(["Drive Name", "Size", "Disk Mark", "Samples", "Rank", "Price", "Drive Value", "Test Date", "Type"])
        for hdd in scraper._hdds: # Iterate over all of the hdd_mega classes
            writer.writerow([hdd._hdd_name, hdd._hdd_size, hdd._hdd_mark, hdd._hdd_samples, hdd._hdd_rank, hdd._hdd_price, hdd._hdd_value, hdd._test_date, hdd._hdd_type]) # Write the row of the data

if __name__ == '__main__':
    ex2csv_get_harddrivebenchmark_single()
    ex2csv_get_harddrivebenchmark_mega()
