# coding: utf-8
import requests
import re
from bs4 import BeautifulSoup
from lxml import html
import csv
import sys
from time import sleep



reload(sys)
sys.setdefaultencoding('utf8')


def getInfos(page, i):
    # Href to items
    articles = page.find_all("h3")
    unit = ""
    poids = ""
    dim = ""
    for item in articles:
        href = "https:" + item.a.get("href")
        name = item.a.text
        result = sessions_requests.get(href)
        soup = BeautifulSoup(result.text, "lxml")
        infos = soup.find_all("span", {"class": "packaging-des"})
        j = 0
        for info in infos:
            if j == 0:
                unit = info.text
            if j == 1:
                poids = info.text
            if j == 2:
                dim = info.text
            if j > 2:
                break
            j += 1

        # Var adjustment
        poids = re.sub(r"(k(.)+.+)\w+", "", poids)
        poids = poids.replace(".)", "")
        poids_float = float(poids)
        dim = re.sub(r"(\(.+\w)\w+", "", dim)
        dim = dim.replace(")", "")
        dim = dim.replace("cm", "")
        name = name.replace(", ", " ")
        # Row create & write in csv
        row = {'index': i, 'nom': name, 'unité': unit, 'poids (en kg)': poids_float, 'dimension (en cm)': dim}
        mywriter.writerow(row)
        i += 1
    return i


# Creating .csv result file
csv_out = open("data.csv", "w+")
fieldnames = ["index", "nom", "unité", "poids (en kg)", "dimension (en cm)"]
mywriter = csv.DictWriter(csv_out, fieldnames=fieldnames)
mywriter.writeheader()


sessions_requests = requests.session()

# Reading research page
# with open("./ali.html", "r") as file:
#     html_doc = file.read()
# page = BeautifulSoup(html_doc, "lxml")

url = "https://fr.aliexpress.com/wholesale?catId=0&initiative_id=SB_20180508030336&SearchText=ecouteurs&smToken=9a715b9cf4314e08a4c3097a2250a384&smSign=KIPiRewo0Somf1e8jtg%2B0Q%3D%3D"
i = 0
while i < 200:
    result = sessions_requests.get(url)
    page = BeautifulSoup(result.text, "lxml")
    try:
        i = getInfos(page, i)
    except:
        print("banishment from Aliexpress")
        quit()
    nextPage = page.find("a", {"class": "page-next"})
    url = "https:" + nextPage.get("href")
    sleep(18)