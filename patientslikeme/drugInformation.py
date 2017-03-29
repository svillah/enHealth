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

def recommendedDosage(soup):
    dosages = soup.find_all("tr", {"data-yah-key":"dosage"})
    ds = []
    for dosage in dosages:
        ds.append(dosage.get('data-yah-value'))
    return ds[0]

def overTheCounter(soup):
    tag = soup.find("p", {"class":"margin-vertical-none"})
    category = tag.find("a").string.encode('utf-8')
    if (category == "Prescription Drugs"):
       return False
    else:
       return True

# execute all above functions to get full drug information     
def getDrugData(url):
    website = url
    soup = initializeSoup(website)

    # removes js and css
    for script in soup(["script", "style"]):
        script.extract()

    # initialize dictionary 
    data = {}
    data["GenericName"] = getGenericName(soup)
    data["OverTheCounter"] = overTheCounter(soup)
    data["BrandName"] = getBrandName(soup)
    data["GeneralDescriptions"] = getDescription(soup)
    data["SideEffects"] = sideEffects(soup)
    data["RecommendedDosage"] = recommendedDosage(soup) 
    data["Source"] = url
    # below are unavailable on patientslikeme.com
    data["Interactions"] = None
    data["ActiveIngredients"] = None
    data["Warnings"] = None

    # writes dictionary to json
    f = open('drugData.json', 'w')
    properIndent = 4
    json.dump(data, f, indent = properIndent)
    f.close()

