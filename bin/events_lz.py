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
        self.baseurl = "http://www.literarisches-zentrum-goettingen.de/programm/"
        # self.baseurl = "file:///home/uschwar1/ownCloud/AC/python/xmpls/events/test/"
        self.today = date.today()
        self.Day = self.today.strftime("%d")
        self.Month = self.today.strftime("%m")
        self.Year = self.today.strftime("%Y")
        (year, month) = divmod(self.today.month, 12)
        self.nextMonth = self.today.replace(year=self.today.year+year, month=month+1, day=1)
        self.NextMonth = self.nextMonth.strftime("%m")
        if int(self.Month) < 6:
            self.thisProg = self.Year + "-1"
        elif int(self.Month) == 6:
            self.thisProg = self.Year + "-1"
            self.nextProg = self.Year + "-2"
        elif int(self.Month) < 12:
            self.thisProg = self.Year + "-2"
        elif int(self.Month) == 12:
            self.thisProg = self.Year + "-2"
            self.nextProg = str(int(self.Year)+1) + "-1"

        self.current_events = self.get_curr_events()


    def get_curr_events(self):
        
        try:
            self.current_events
        except:
            self.current_events = {}
        url = self.baseurl + self.thisProg + "/hauptprogramm/"
        # url = self.baseurl + "literarisches-zentrum-goettingen-programm-" + self.thisProg + ".html"
        self.get_events(url, self.current_events, self.Year,self.Month,self.Day)
        if int(self.Month) == 6:
            url = self.baseurl + self.nextProg + "/hauptprogramm/"
            self.get_events(url, self.current_events, self.Year,self.Month,self.Day)
        elif int(self.Month) == 12:
            url = self.baseurl + self.nextProg + "/hauptprogramm/"
            self.get_events(url, self.current_events, self.Year+1,self.Month,self.Day)
            
        return self.current_events


    
    def get_events(self,url,curr_events,year,month,day):
        mech = Browser()
        print "WARNING: HTTP Error 403: request disallowed by robots.txt"
        print "!!! ask Provider !!!"
        mech.set_handle_robots(False)
        mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        RR = mech.open(url)
        webpage = RR.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        table = soup.findAll("div",{"class":"event hauptprogramm"})
        
        for row in table:#[1:]: 
            dt = row.find("p",{"class":"datetime"})
            pr = row.find("div",{"class":"presentation"})
            ref = dt.find("a", href=True)["href"]
            daymnth =  dt.find("span",{"class":"day"})
            DayMnth = daymnth.text.strip()
            Day = DayMnth.split(" ")[0].replace(".","")
            Month = str(self.months.index(DayMnth.split(" ")[1][:-1]) + 1)
            Time = daymnth.next_sibling.strip().replace(" ","").replace("Uhr","")[:-1]
            Hour = Time.split(":")[0]#.encode("utf-8")
            Mnte = Time.split(":")[1]#.encode("utf-8")
            # print ref
            # print Day, Month, Hour, Mnte
            date = str(year) + "-" + Month + "-" + Day
            time = Hour + ":" + Mnte
            
            subtitle =  pr.find("span",{"class":"guests"}).text.strip().replace("\t","").replace("\n","")
            title =  pr.find("strong",{"class":"title"}).text.strip()
            more = pr.find("div",{"class":"text"}).text.strip()
            loc = row.find("div",{"class":"location"})
            place = loc.find("a").text.strip()
            text =  loc.find("span").text.strip()
            etime =""
            # print "Guests ", subtitle, "\nTitle ", title, "\nText ", text, "\nPlace ", place, "\nMore ", more
            if title != "":
                cont = {"date" : date, "time" : time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : ref, "place" : place}
                curr_events[str(date) + "_" + time +  "_" + place.replace(" ","").split(",")[0]] = cont
        return curr_events



##########################
if __name__ == '__main__':
    evt = events()
    print evt.current_events

    
