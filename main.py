#!/usr/bin/python3.8

import time
import xlsxwriter

# import csv
import requests
from bs4 import BeautifulSoup as bs

HOST = "https://www.amazon.ae/s?k={}&ref=nb_sb_noss"
workbook = xlsxwriter.Workbook("./out/prices.xlsx")
worksheet = workbook.add_worksheet()
# errOut = open("./out/errors.csv", "w");
# errWriter = csv.writer(errOut);


def fillList():
    asinList = []
    with open("./input.txt") as f:
        content = f.readlines()
    asinList = [x.strip() for x in content]
    # remove \n from end
    return asinList


def writeExcel(asin, price, currency, number):
    worksheet.write("A{}".format(number), asin)
    worksheet.write("B{}".format(number), price)
    worksheet.write("C{}".format(number), currency)


def amazonSearch(asin_list):
    number = 0
    for asin in asin_list:
        number += 1
        if number % 25 == 0:  # some feedback to make sure it isn't stuck
            print("Finished {}. Currently at {}".format(number, asin))
        req = requests.get(HOST.format(asin))
        while req.status_code == 503:  # sometimes requests fucks up
            req = requests.get(HOST.format(asin))
            time.sleep(0.5)
            # Don't spam
        if req.status_code != 200:
            print(
                "Something happened while getting {}. Moving on!!".format(
                    HOST.format(asin)
                )
            )
            continue
        soup = bs(req.content, "html.parser")
        products = soup.find_all("div", {"class": "s-asin"})
        if len(products) == 0:
            writeExcel(asin, "N/A", "N/A", number)
            continue
        price = products[0].find("span", "a-offscreen")
        if price:
            currency, price = price.text.split()
        else:
            writeExcel(asin, "N/A", "N/A", number)
            continue
        writeExcel(asin, price, currency, number)


def main():
    print("Reading ASIN List!")
    asinList = fillList()
    print("Starting search!")
    amazonSearch(asinList)
    print("Done!!")


main()

# errOut.close();
workbook.close()
