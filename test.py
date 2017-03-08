import urllib
import json
import requests
from bs4 import BeautifulSoup

def initializeSoup(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def getGenericName(soup):
    genericName = soup.h1.span.string.encode('utf-8')
    return genericName

def getBrandName(soup):
    brandNames = soup.find("span", {"class":"comma-separated"})
    bn = []
    if(brandNames is None):
        return ("None Available")
    else:
        brandNames = brandNames.find_all('a')
        for brand in brandNames:
            bn.append(brand.string.rstrip().encode('utf-8'))
        return bn
            
def getDescription(soup):
    desc = soup.find("p",{"itemprop":"description"})
    return desc.string.rstrip().encode('utf-8')

def sideEffects(soup):
    sideEffects = soup.find_all("tr", {"data-yah-key":"side_effect"})
    se = []
    for sideEffect in sideEffects:
        lis = sideEffect.find("span", {"itemprop":"name"})
        se.append(lis.string.encode('utf-8'))
    return se

    # below are not implemented
    # RecommendedDosage TBD

    # OverTheCounter

    # Interactions

    # Side effects paragraph

    # Usage

    # Active ingredients

    # Warnings

    # Source

def getDrugData(url, f):
    website = url
    soup = initializeSoup(website)

    # removes js and css
    for script in soup(["script", "style"]):
        script.extract()

    # initialize dictionary 
    data = {}
    data["GenericName"] = getGenericName(soup)
    data["BrandName"] = getBrandName(soup)
    data["GeneralDescriptions"] = getDescription(soup)
    data["SideEffects"] = sideEffects(soup)

    # writes dictionary to json
    json.dump(data, f, indent=4)

# get URLs of all drugs, note that this is only page one
website = "https://www.patientslikeme.com/treatments/browse?cat=1"
soup = initializeSoup(website)
drugTable = soup.find("table", {"id":"tbl-treatments"})
drugs = drugTable.findChildren('tr')
f = open('drugData.json', 'w')

# for i in range(1, len(drugs)):
for i in range(1,7):
    for drugUrl in drugs[i].findChildren("a"):
        url = drugUrl.get("href")
        fullUrl = "https://www.patientslikeme.com" + url
        # go to URL for each drug and obtain info
        getDrugData(fullUrl, f)

f.close()


