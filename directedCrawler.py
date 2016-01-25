import urllib, sgmllib
from bs4 import BeautifulSoup
import time
class MyParser(sgmllib.SGMLParser):
    "A simple parser class."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()
        
    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."
        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []

    def start_a(self, attributes):
        for name,value in attributes:
            
            if name == "href" and "/wiki" in value and ":" not in value and "//" not in value and "Main_Page" not in value:
                if ("https://en.wikipedia.org"+value) not in self.hyperlinks:
                    self.hyperlinks.append("https://en.wikipedia.org"+value)
    def get_hyperlinks(self):
        return self.hyperlinks

# Start node for the crawling
seed="https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
#The list of URL's which contain the keyword
URLlist=[]
#The list of URL's which have to be crawled on
unVisited=[seed]
# intitializing the Parser
myparser=MyParser()
# Keyword to be looked up when crawling a page
keyword="concordance"
# distance between the current page and the seed page (number of hops between them)
level=0
#dictionary containing the url as key and the number of hops as a distance
distance={seed:level}
#lower casing the keyword to make it independent of the casing
keyword=keyword.lower()

#checking each node of the unVisited array, the array is appended with a links found on the crawling page
# if the number of links containing the keyword in 1000, crawling is stopped
while(len(unVisited)>0 and len(URLlist)<1000):
    # taking the FIRST element of the unVisited URL list
    #done so that the pages with lesser hops are checked first
    url=unVisited.pop(0)
    #if the page has already been added to URL list, skip the URL
    if(url in URLlist):
        continue
    #Checking the level of the page
    url_level=distance.get(url)
    #if the page distance from the Seed URL is less than 5 , then crawl the page
    if(url_level<5):
        #open the URL and get its text format
        while True:
            try:
                f = urllib.urlopen(url)
            except IOError:
                time.sleep(20)
                pass
            else:
                break
        #time.sleep(1)
        s = f.read()
        soup=BeautifulSoup(s)
        text=soup.get_text()
        # if the keyword exsists in the page, crawl
        #making the text smaller case to make the search case independent
        if (keyword in text.lower()):
            print "Crawling: ", url," Level", url_level
            URLlist.append(url)
            #using the parser to get the hyperlinks on that page
            myparser.parse(s)
            hyperlinks=myparser.get_hyperlinks()
            #add the child URL's on that page to the list of unVisited array
            # mark the level of the URL in the dictionary
            for subUrl in hyperlinks :
                unVisited.append(subUrl)
                distance[subUrl]=distance.get(subUrl,(url_level+1))
            print len(hyperlinks)," ",len(unVisited)
    
print len(URLlist)," ",len(unVisited)
for x in URLlist:
    print x," ",distance[x]
