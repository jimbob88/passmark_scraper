# -*- coding: utf-8 -*-
from passmark_scraper import cpubenchmark
import csv

def ex2csv_get_cpubenchmark_single():
    """
    Export the cpubenchmark single cpu system scrape to a csv file
    """
    scraper = cpubenchmark.cpubenchmark_scraper_single() # Initiliaze the cpubenchmark_scraper_single class
    scraper.refresh_all() # Refresh the web page, and scrape all of its data into scraper._cpus

    with open('cpubenchmark_single.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f) # Create new csv writer instance
        writer.writerow(["CPU Name", "Passmark CPU Mark (higher is better)", "Rank (lower is better)", "CPU Value (higher is better)", "Price (USD)"]) # Write the headings for the csv
        for cpu in scraper._cpus: # Iterate over all of the cpu_single classes
            writer.writerow([cpu._name, cpu._mark, cpu._rank, cpu._value, cpu._price]) # Write the row of the data

def ex2csv_get_cpubenchmark_mega():
    """
    Export the cpubenchmark mega cpu scrape to a csv file
    """
    scraper = cpubenchmark.cpubenchmark_scraper_mega() # Initiliaze the cpubenchmark_scraper_mega class
    scraper.refresh_all() # Refresh the web page, and scrape all of its data into scraper._cpus

    with open('cpubenchmark_mega.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f) # Create new csv writer instance
        writer.writerow(["CPU Name", "Price", "CPU Mark", "CPU Value", "Thread Mark", "Thread Value", "TDP (W)", "Power Perf.", "Test Date", "Socket", "Category"])
        for cpu in scraper._cpus: # Iterate over all of the cpu_mega classes
            writer.writerow([cpu._cpu_name, cpu._cpu_price, cpu._cpu_mark, cpu._cpu_value, cpu._thread_mark, cpu._thread_value, cpu._tdp, cpu._power_perf, cpu._test_date, cpu._socket, cpu._category]) # Write the row of the data

if __name__ == '__main__':
    ex2csv_get_cpubenchmark_single()
    ex2csv_get_cpubenchmark_mega()
