import urllib
from bs4 import BeautifulSoup

# initializes html doc
testfile = "gabapentin.html"
html = urllib.urlopen(testfile).read()
soup = BeautifulSoup(html, 'html.parser')

# removes js and css 
for script in soup(["script", "style"]):
    script.extract()

# sample outputs
print(soup.h2.string)
print(soup.find_all('a'))
