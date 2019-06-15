import sys
from mechanize import Browser
import string
from bs4 import BeautifulSoup
import csv
from datetime import date

class events:

    def __init__(self):
        self.baseurl = "http://www.junges-theater.de/spielplan/"
        # self.baseurl = "file:///home/uschwar1/ownCloud/AC/python/xmpls/events/test/"
        self.today = date.today()
        self.Day = self.today.strftime("%d")
        self.Month = self.today.strftime("%m")
        self.Year = self.today.strftime("%Y")

        self.current_events = self.get_curr_events()
        
        (year, month) = divmod(self.today.month + 1, 12)
        self.Month = str(self.today.month + 1)
        self.Year = str(int(self.Year) + year)
        self.current_events = self.get_curr_events()
         
    def get_curr_events(self):
        
        try:
            self.current_events
        except:
            self.current_events = {}
        url = self.baseurl + "?month=" + self.Month
        # url = self.baseurl + "jt-spielplan-month" + self.Month + ".html"
        self.get_events(url, self.current_events, self.Year,self.Month,self.Day)
            
        return self.current_events


    
    def get_events(self,url,curr_events,year,month,day):
        mech = Browser()
        mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        RR = mech.open(url)
        webpage = RR.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        table = soup.findAll("div",{"class":"row dark"})
        
        for row in table:#[1:]:
            divs0 = row.findAll("div")
            Day = divs0[0].text.split(".")[0][1:]
            Month = divs0[0].text.split(".")[1]
            date = str(year) + "-" + Month + "-" + Day
            divs00 = divs0[1].findAll("div")
            time = divs00[0].text.replace("Uhr","").strip()
            refpart = divs00[1].find("a", href=True)
            ref = refpart["href"]
            title = refpart.text
            subtitle = divs00[1].find("p").text[:-2]
            place = "Junges Theater"
            
            text = ""
            etime = ""
            if title != "":
                cont = {"date" : date, "time" : time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : ref, "place" : place}
                curr_events[str(date) + "_" + time +  "_" + place.replace(" ","").split(",")[0]] = cont
            cont_csv = date + ";" + time + ";" + etime + ";" + title + ";" + subtitle + ";" + text + ";" +  ref + ";" +  place
            print cont_csv
        return curr_events



            # for ref in refs:
            #     print ref["href"]


        sys.exit(0)
        for row in table:#[1:]: 
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
            
            subtitle =  pr.find("span",{"class":"guests"}).text.strip().replace("\t","").replace("\n","").encode("utf-8")
            title =  pr.find("strong",{"class":"title"}).text.strip().encode("utf-8")
            more = pr.find("div",{"class":"text"}).text.strip().encode("utf-8")
            loc = row.find("div",{"class":"location"}).encode("utf-8")
            place = loc.find("a").text.strip().encode("utf-8")
            text =  loc.find("span").text.strip().encode("utf-8")
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

    
