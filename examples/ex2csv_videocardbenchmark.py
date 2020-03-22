# -*- coding: utf-8 -*-
from passmark_scraper import videocardbenchmark
import csv

def ex2csv_get_videocardbenchmark_single():
    """
    Export https://www.videocardbenchmark.net/gpu_list.php to a csv file
    """
    scraper = videocardbenchmark.videocardbenchmark_scraper_single() # Initiliaze the videocardbenchmark_scraper_single class
    scraper.refresh_all() # Refresh the web page, and scrape all of its data into scraper._gpus

    with open('videocardbenchmark_single.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f) # Create new csv writer instance
        writer.writerow(["Videocard Name", "Passmark G3D Mark (higher is better)", "Rank (lower is better)", "Videocard Value (higher is better)", "Price (USD)"]) # Write the headings for the csv
        for gpu in scraper._gpus: # Iterate over all of the gpu_single singles
            writer.writerow([gpu._gpu_name, gpu._gpu_mark, gpu._gpu_rank, gpu._gpu_value, gpu._gpu_price]) # Write the row of the data

def ex2csv_get_videocardbenchmark_mega():
    """
    Export https://www.videocardbenchmark.net/GPU_mega_page.html to a csv file
    """
    scraper = videocardbenchmark.videocardbenchmark_scraper_mega() # Initiliaze the videocardbenchmark_scraper_mega class
    scraper.refresh_all() # Refresh the web page, and scrape all of its data into scraper._gpus

    with open('videocardbenchmark_mega.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f) # Create new csv writer instance
        writer.writerow(["Videocard Name", "Price", "G3D Mark", "Videocard Value", "G2D Mark", "TDP (W)", "Power Perf.", "Test Date", "Category"])
        for gpu in scraper._gpus: # Iterate over all of the gpu_mega classes
            writer.writerow([gpu._gpu_name, gpu._gpu_price, gpu._gpu_mark, gpu._gpu_value, gpu._g2d_mark, gpu._tdp, gpu._power_perf, gpu._test_date, gpu._category]) # Write the row of the data

if __name__ == '__main__':
    ex2csv_get_videocardbenchmark_single()
    ex2csv_get_videocardbenchmark_mega()
