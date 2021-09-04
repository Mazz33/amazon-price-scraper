# amazon-price-scraper
Super Basic Amazon Scraper. Using list of ASIN will give back prices in excel format

## Requirements
Libraries needed: `requests`, `bs4`, `xlsxwriter`

## Input
Expects text file of ASIN numbers seperated by new line. Named `input.txt` in the same folder as main.py

## output
Output will be in out/ folder under excel file named `prices.xlsx` It will overwrite existing data so care.

## Running
For linux simply `chmod +x main.py` -> `./main.py`  
Else `python3.8 main.py`
