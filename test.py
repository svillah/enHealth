import urllib
import json
import requests
from bs4 import BeautifulSoup

f = open('drugData.json', 'w+')

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
    f.write("\n{ \n\"GenericName\" : \"" + genericName + "\"\n")

    # finds common brands
    brandNames = soup.find("span", {"class":"comma-separated"})
<<<<<<< HEAD
    f.write("Brand Names:")
    if(brandNames is None):
        f.write("None Available")
    else:
        brandNames = brandNames.find_all('a')
        for brand in brandNames:
            f.write(brand.string.rstrip().encode('utf-8')) #rstrip removes all new lines \n
=======
    brandName = brandNames.find_all('a')
    f.write("\"BrandName\" : ")
    for brand in brandNames:
        f.write(brand.string.rstrip().encode('utf-8')) #rstrip removes all new lines \n
>>>>>>> 42854a029dbb0fe3f52a88681c2680249fef0fb9

    # finds drug description
    desc = soup.find("p",{"itemprop":"description"})
    f.write("\n\"GeneralDescriptions\" : " + desc.string.encode('utf-8'))

    # finds side effects of taking drug
    sideEffects = soup.find_all("tr", {"data-yah-key":"side_effect"})
    f.write("\"SideEffectsList\" : ")

    for sideEffect in sideEffects:
        lis = sideEffect.find("span", {"itemprop":"name"})
        f.write("\"" + lis.string.encode('utf-8') + "\", ")
    f.write("\n},")

    # below are not implemented
    # RecommendedDosage TBD

    # OverTheCounter

    # Interactions

    # Side effects paragraph

    # Usage

    # Active ingredients

    # Warnings

    # Source

website = "https://www.patientslikeme.com/treatments/browse?cat=1"
soup = initializeSoup(website)
#button for next page
disabled = soup.find("a", {"class":"button icon-only is-not-rwd next_page",
                           "disabled":"true"})
#checks to see if there is only one page
if(disabled is not None):
    drugTable = soup.find("table", {"id":"tbl-treatments"})
    drugs = drugTable.findChildren('tr')
    #iterate through each drug on the page
    for i in range(1, len(drugs)):
    #for i in range(1, 3): # use code above for actual implementation, current for test
        for drugUrl in drugs[i].findChildren("a"):
            url = drugUrl.get("href")
            fullUrl = "https://www.patientslikeme.com" + url
            # go to URL for each drug and obtain info
            getDrugData(fullUrl)
else:
    #loop iterates through each page until it reaches the last page
    pageNum = 1
    while(disabled is None):
        # get URLs of all drugs
        website = "https://www.patientslikeme.com/treatments/browse?cat=1&page=" + str(pageNum).encode('utf-8')
        soup = initializeSoup(website)
        drugTable = soup.find("table", {"id":"tbl-treatments"})
        drugs = drugTable.findChildren('tr')
        disabled = soup.find("a", {"class":"button icon-only is-not-rwd next_page",
                               "disabled":"true"})    
        #iterate through each drug on the page
        for i in range(1, len(drugs)):
        #for i in range(1, 3): # use code above for actual implementation, current for test
            for drugUrl in drugs[i].findChildren("a"):
                url = drugUrl.get("href")
                fullUrl = "https://www.patientslikeme.com" + url
                # go to URL for each drug and obtain info
                getDrugData(fullUrl)
        pageNum += 1
#end program
f.close()
