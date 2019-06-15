import sys
from mechanize import Browser
import string
from bs4 import BeautifulSoup
import csv
from datetime import date

class events:

    months = [
        "Januar",
        "Februar",
        "M\xc3\xa4rz".decode("utf-8"),
        "April",
        "May",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "Dezember"
    ]
    def __init__(self):
        self.baseurl = "http://www.filmfest-goettingen.de/"
        # self.baseurl = "file:///home/uschwar1/ownCloud/AC/python/xmpls/events/test/"
        self.today = date.today()
        self.Day = self.today.strftime("%d")
        self.Month = self.today.strftime("%m")
        self.Year = self.today.strftime("%Y")
        (year, month) = divmod(self.today.month, 12)
        self.nextMonth = self.today.replace(year=self.today.year+year, month=month+1, day=1)
        self.NextMonth = self.nextMonth.strftime("%m")

        self.current_events = self.get_curr_events()


    def get_curr_events(self):
        
        try:
            self.current_events
        except:
            self.current_events = {}
        url = self.baseurl
        # url = self.baseurl + "XYZ-programm-" + self.thisProg + ".html"
        self.get_events(url, self.current_events, self.Year,self.Month,self.Day)

        return self.current_events


    
    def get_events(self,url,curr_events,year,month,day):
        mech = Browser()
        # mech.set_handle_robots(False)
        mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        RR = mech.open(url)
        webpage = RR.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        table = soup.find("div",{"id":"navigation"})
        ul = table.find("ul")
        for li in ul.findAll("li"):
            liref = li.find("a", href=True)["href"]
            if liref.endswith("programm.html"):
                nexturl = url + liref
        print nexturl
        nexturldir = nexturl[0:nexturl.rfind("/")+1]
        print nexturldir
        nextRR = mech.open(nexturl)
        nextwebpage = nextRR.read()
        nextsoup = BeautifulSoup(nextwebpage, 'html.parser')
        # print nextsoup.text
        nexttable0 = nextsoup.find("div",{"id":"container"})
        nexttable1 = nexttable0.find("div",{"id":"content"})
        nexttable2 = nexttable1.find("div",{"id":"tage"})
        ul = nexttable2.find("ul")
        for li in ul.findAll("li"):
            liref = li.find("a", href=True)["href"]
            nnextRR = mech.open(nexturldir + liref)
            nnextwebpage = nnextRR.read()
            nnextsoup = BeautifulSoup(nnextwebpage, 'html.parser')
            # print nnextsoup.text
            nnexttable0 = nnextsoup.find("div",{"id":"container"})
            nnexttable1 = nnexttable0.find("div",{"id":"content"})
            nnexttable2 = nnexttable1.find("div",{"class":"timeTable"})
            datestr = nnexttable2.find("h1").text
            datelist = datestr.split(",")[1].strip().split(".")
            day = datelist[0]
            if len(day) == 1:
                day = "0" + day
            month = datelist[1]
            if len(month) == 1:
                month = "0" + month
            year = datelist[2]
            print day, month, year
            date = str(year) + "-" + month + "-" + day
            itemlist_h = nnexttable2.findAll("h2")
            itemlist_a = nnexttable2.findAll("a", href=True)
            itemlist_p = nnexttable2.findAll("p")
            for i in range(len(itemlist_h)):
                time = itemlist_h[i].text.split("Uhr")[0].strip()
                place = itemlist_h[i].text.split("Uhr")[1].replace("im","").replace("in der","").strip()
                try:
                    ref = itemlist_a[i]["href"]
                    title = itemlist_a[i].text
                except:
                    ref = ""
                    title = ""
                try:
                    subtitle = itemlist_p[i].text
                except:
                    subtitle = ""
        etime = ""
        text = ""
        cont = {"date" : date, "time" : time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : ref, "place" : place}
        self.current_events[str(date) + "_" + time +  "_" + place.replace(" ","")] = cont
        return curr_events

##########################
if __name__ == '__main__':
    evt = events()
    print evt.current_events

