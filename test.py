import urllib
import json
import requests
from bs4 import BeautifulSoup

f = open('drugData.json', 'a+')

def initializeSoup(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def getDrugData(url):
    website = url
    soup = initializeSoup(website)

    # removes js and css
    for script in soup(["script", "style"]):
        script.extract()

    # finds generic drug name
    genericName = soup.h1.span.string
    f.write("\nGeneric Name: " + genericName + "\n")

    # finds common brands
    brandNames = soup.find("span", {"class":"comma-separated"})
    brandName = brandNames.find_all('a')
    f.write("Brand Names:")
    for brand in brandNames:
        f.write(brand.string.rstrip(),) #rstrip removes all new lines \n

    # finds drug description
    desc = soup.find("p",{"itemprop":"description"})
    f.write("\nGeneral Description: " + desc.string)

    # finds side effects of taking drug
    sideEffects = soup.find_all("tr", {"data-yah-key":"side_effect"})
    f.write("Side Effects: ")

    for sideEffect in sideEffects:
        lis = sideEffect.find("span", {"itemprop":"name"})
        f.write(lis.string)
    f.write("\n")

    # below are not implemented
    # RecommendedDosage TBD

    # OverTheCounter

    # Interactions

    # Side effects paragraph

    # Usage

    # Active ingredients

    # Warnings

    # Source

# get URLs of all drugs, note that this is only page one
website = "https://www.patientslikeme.com/treatments/browse?cat=1"
soup = initializeSoup(website)
drugTable = soup.find("table", {"id":"tbl-treatments"})
drugs = drugTable.findChildren('tr')

#for i in range(1, len(drugs)):
for i in range(1, 3): # use code above for actual implementation, current for test
    for drugUrl in drugs[i].findChildren("a"):
        url = drugUrl.get("href")
        fullUrl = "https://www.patientslikeme.com" + url
        # go to URL for each drug and obtain info
        getDrugData(fullUrl)

f.close()
