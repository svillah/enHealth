import urllib
from bs4 import BeautifulSoup

# initializes html doc
testfile = "gabapentin.html"
html = urllib.urlopen(testfile).read()
soup = BeautifulSoup(html, 'html.parser')

# removes js and css 
for script in soup(["script", "style"]):
    script.extract()

# finds generic drug name
genericName = soup.h1.span.string
print "Generic Name: " + genericName + "\n"

# finds common brands 
brandNames = soup.find("span", {"class":"comma-separated"})
brandName = brandNames.find_all('a')

print "Brand Names:" 
for brand in brandNames:
    print brand.string.rstrip(), #rstrip removes all new lines \n

# finds drug description
desc = soup.find("p",{"itemprop":"description"})
print "\n \nGeneral Description: " + desc.string 

# finds side effects of taking drug
sideEffects = soup.find_all("tr", {"data-yah-key":"side_effect"})
print "Side Effects: "

for sideEffect in sideEffects:
    lis = sideEffect.find("span", {"itemprop":"name"})
    print lis.string

# below are not implemented
# RecommendedDosage TBD

# OverTheCounter

# Interactions

# Side effects paragraph

# Usage

# Active ingredients

# Warnings

# Source

