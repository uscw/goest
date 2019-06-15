import sys
from mechanize import Browser
import string
from bs4 import BeautifulSoup
import csv
from datetime import date

class events:

    def __init__(self):
        self.baseurl = "http://www.lumiere.de/"
        # self.baseurl = "file:///home/uschwar1/ownCloud/AC/python/xmpls/events/test/"
        self.today = date.today()
        self.Day = self.today.strftime("%d")
        self.Month = self.today.strftime("%m")
        self.Year = self.today.strftime("%Y")
        (year, month) = divmod(self.today.month, 12)
        self.nextMonth = self.today.replace(year=self.today.year+year, month=month+1, day=1)
        self.NextMonth = self.nextMonth.strftime("%m")
        self.current_events = self.get_curr_events(self.today.year,self.today.month,self.today.day)


    def get_curr_events(self,year,month,day):

        items_visited = {}
        try:
            self.current_events
        except:
            self.current_events = {}

        #get main page
        url = self.baseurl # + "index.html"
        mech = Browser()
        mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        RR = mech.open(url)
        webpage = RR.read()
        soup = BeautifulSoup(webpage, 'html.parser')

        linksFrame = soup.find('frame', {'name':'Links'})

        # get zeitplan page
        url = self.baseurl + linksFrame["src"]
        mech = Browser()        
        RR = mech.open(url)
        webpage = RR.read()
        soup = BeautifulSoup(webpage, 'html.parser')

        tables = soup.findAll("table")
        
        dates = tables[1].findAll("th", {'class':'date'} )
        for Date in dates:
            nextNode = Date
            datestr = Date.text
            try:
                Day = datestr.split(" ")[1].split(".")[0]
                Month = datestr.split(" ")[1].split(".")[1]
            except:
                continue
            if len(Day) == 1:
                Day = "0" + Day 
            if len(Month) == 1:
                Month = "0" + Month
            date = str(year) + "-" + Month + "-" + Day
            while True:
                try:
                    nextNode = nextNode.next_sibling
                    if nextNode.text == "" or nextNode.find("th") != None:
                        break
                    Time = nextNode.text.split("Uhr")[0].replace(" ","").split(".")
                    hour = Time[0]
                    if len(hour) == 1:
                        hour = "0" + hour
                    if len(Time) == 2:
                        minute = Time[1]
                    else:
                        minute = "00"
                    time = hour + ":" + minute
                except:
                    break
                try:
                    ref = nextNode.find("a")["href"].replace("../","")
                except:
                    None
                try:
                    visited = items_visited[ref]
                    text = visited["text"]
                    title = visited["title"]
                    subtitle = visited["subtitle"]
                except:
                    # get more info from reference
                    url = self.baseurl + ref
                    # url = self.baseurl + "18/11/disturbing.htm"
                    mech = Browser()        
                    RR = mech.open(url)
                    webpage = RR.read()
                    soup = BeautifulSoup(webpage, 'html.parser')
                    title = soup.find("h2").text
                    br = soup.find("h3").find('br')
                    text = br.nextSibling
                    subtitle = br.previousSibling
                    items_visited[ref] = { "title" : title, "subtitle" : subtitle, "text" : text }
                place = "Lumiere"
                etime = "" 
                cont = {"date" : date, "time" : time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : ref, "place" : place}
                self.current_events[str(date) + "_" + time +  "_" + place.replace(" ","")] = cont
        
        return self.current_events
        #print len(dates), dates
        #print len(contents), contents
        

##########################
if __name__ == '__main__':
    evt = events()
    print(evt.current_events)
