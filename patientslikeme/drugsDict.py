from bs4 import BeautifulSoup
import requests
import urllib

def initializeSoup(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def getDrugName(url):
    soup = initializeSoup(url)
    #removes js and css
    for script in soup (["script", "style"]):
        script.extract()
    return soup.h1.span.string
    
def addBrandNames(url,dictionary):
    soup = initializeSoup(url)
    brandNames = soup.find("span", {"class":"comma-separated"})
    if(brandNames is not None):
        brandNames = brandNames.find_all('a')
        #print(brandNames)
        for brand in brandNames:
            url = brand.get("href")
            fullUrl = "https://www.patientslikeme.com" + url
            name = brand.string.rstrip().encode('utf-8')
            dictionary[name] = fullUrl

def addToDict(drugs,drugDict,onePage):
    for i in range(1, len(drugs)):
        for drugUrl in drugs[i].findChildren("a"):
            url = drugUrl.get("href")
            fullUrl = "https://www.patientslikeme.com" + url
            # go to URL for each drug, add each name and associating url to the dictionary
            drugDict[getDrugName(fullUrl)] = fullUrl
            if(not onePage):
                addBrandNames(fullUrl,drugDict)

#this will be our drug dicitonary
drugDict = {}
website = "https://www.patientslikeme.com/treatments/browse?cat="

#creating dictionary for drugs
drugDict = {}
prescriptionDrugs = 1
overTheCounterDrugs = 2
allCat = [prescriptionDrugs,overTheCounterDrugs]
for category in allCat:
    soup = initializeSoup(website + str(category).encode('utf-8'))
    #button for next page
    disabled = soup.find("a", {"class":"button icon-only is-not-rwd next_page",
                               "disabled":"true"})
    #checks to see if there is only one page
    if(disabled is not None):
        drugTable = soup.find("table", {"id":"tbl-treatments"})
        drugs = drugTable.findChildren('tr')
        onePage = True
        #iterate through each drug on the page and add it to the dictionary
        addToDict(drugs,drugDict,onePage)
    else:
        #loop iterates through each page until it reaches the last page
        pageNum = 1
        while(pageNum < 2): #value set for testing purposes, change when done
            #print(pageNum)
            # get URLs of all drugs
            website = "https://www.patientslikeme.com/treatments/browse?cat=" + str(category).encode('utf-8') + "&page=" + str(pageNum).encode('utf-8')
            soup = initializeSoup(website)
            drugTable = soup.find("table", {"id":"tbl-treatments"})
            drugs = drugTable.findChildren('tr')
            disabled = soup.find("a", {"class":"button icon-only is-not-rwd next_page",
                                   "disabled":"true"})    
            onePage = False
            #iterate through each drug on the page and add it to the dictionary
            addToDict(drugs,drugDict,onePage)
            pageNum += 1


