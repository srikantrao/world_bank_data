"""
Download documents as .txt files and then generate csv files for some of the tables 
"""

import argparse 
import numpy as np
import pandas as pd 
import xlrd
import os 
import wget 
import requests
from bs4 import BeautifulSoup, SoupStrainer
import glob
import sys

# Load xls file and output a list of urls
def  read_url(xlsx):
    """
    :param xls - Path to the xls file 
    :returns - A dictionary. Key: url_string and Value: url link
    """

    # Create an Excel Worksheet Object for the correct worksheet
    wb = xlrd.open_workbook(xlsx)
    ws = wb.sheet_by_index(0)

    # URL dictionary to store all the data.
    url_dict = {}

    # Get hold of the xls filename. A folder called {filename} will be created which will
    # have all the .txt files inside of it.
    xls_path = xlsx.split(".")[-2].split("/")[-1]

    # Create a folder if it does not exist
    if not os.path.exists(f"txt_files/{xls_path}"):
        os.makedirs(f"txt_files/{xls_path}")
        print(f"Create a new directory at ./txt_files/{xls_path}")

    # Iterate over all the rows 
    for row in range(1, ws.nrows):
        # Find the url information stored in the last column of the excel sheet in this case.
        url_string = ws.cell(row, 6).value
        case_number = "Case_" + str(int(ws.cell(row, 0).value))

        # Make sure that the url is not NoneType
        if url_string and "NA" not in url_string:

            txt_link = look_for_txt_url(url_string)
            print(txt_link)

            if not txt_link:
                print(f"No .txt file was found at {url_string}")
                continue

            url_dict[url_string] = "http://documents.worldbank.org" + txt_link
            print(f"\nRow: {row} with url: {url_dict[url_string]} and filename {case_number}.txt")
            try:
                wget.download(url_dict[url_string], f"txt_files/{xls_path}/{case_number}.txt")
            except OSError or FileNotFoundError:
                print(f"There was a problem in file: {case_number}")
        else:
            print(f"url_string was not generated because of a problem. Please take another look at this link.")
    
    print(f"{ws.nrows} numbers of rows were parsed")
    return url_dict

def look_for_txt_url(url_link):
    """
    Look for .txt urls in the url_link web page 
    """
    content = requests.get(url_link).content
    soup = BeautifulSoup(content, parse_only = SoupStrainer('a'), features="html.parser")

    for link in soup:
        if hasattr(link, "href") and 'txt' in link["href"]:
            return link['href']

    # If you could not find the txt url then return a NoneType object
    return None
    
def convert_url(url_link):
    """
    Modify the url so that the .txt can be downloaded. 
    Here is an example modification - 
    
    Original - http://documents.worldbank.org/curated/en/574611569875990987/Restructuring-Integrated-Safeguards-Data-Sheet-IN-Rural-Water-Supply-and-Sanitation-Project-for-Low-Income-States-P132173
    
    Modified - http://documents.worldbank.org/curated/en/574611569875990987/text/Restructuring-Integrated-Safeguards-Data-Sheet-IN-Rural-Water-Supply-and-Sanitation-Project-for-Low-Income-States-P132173.txt
    
    The point is to add the additional 'text' and the .txt at the end.
    """
    index  = url_link.rfind("/")
    mod_url = url_link[: index] + "/text" + url_link[index:]
    
    # Add the txt to the end of the url 
    return f"{mod_url}.txt"

def download_url(url_dict, download_path):
    """
    Download all the text file that the url_dict items points to.
    """
    for url_string, url_link in url_dict.items():
        if url_link:
            try:
                wget.download(url_link, f"{download_path}/{url_string}.txt")
            except OSError or FileNotFoundError:
                print(f"There was a problem in file: {url_string}")

def main():

    xls_list = glob.glob("./data/*.xls")

    for xls_file in xls_list:

        print(f"Reading files from: {xls_file}")

        url_dict = read_url(xls_file)
        # download_url(url_dict, f"./txt_files")

    # xls_list = "./data/ISDS_1to1200.xls"
    # url_dict = read_url(xls_list)
    # download_url(url_dict, "txt_files/ISDS_1to1200")
    

if __name__ == "__main__":


    # Run
    main()
