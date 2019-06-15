import sys
from mechanize import Browser
import string
from bs4 import BeautifulSoup
import csv
from datetime import date

class events:

    def __init__(self):
        self.baseurl = "https://www.dt-goettingen.de/kalender/"
        # self.baseurl = "file:///home/uschwar1/ownCloud/AC/python/xmpls/events/test"
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
        url = self.baseurl + "/?mo=" + self.Month + "&ye=" + self.Year + "&fi="
        # url = self.baseurl + "/dt_" + str(year) + str(month) + ".html"
        self.get_monthly_events(url, self.current_events, self.Year,self.Month,self.Day)
        url = self.baseurl + "/?mo=" + self.nextMonth.strftime("%m") + "&ye=" + self.nextMonth.strftime("%Y") + "&fi="
        # url = self.baseurl + "/dt_" + str(year) + str(month+1) + ".html"
        self.get_monthly_events(url, self.current_events, self.Year,self.NextMonth,self.Day)
        return self.current_events

    def get_monthly_events(self,url,curr_events,year,month,day):
        mech = Browser()
        mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        RR = mech.open(url)
        webpage = RR.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        table = soup.find(id="spielplan")
            
        for row in table.findAll('tr'):#[1:]: 
            col = row.findAll('td')
            s0 = col[0]
            s1 = col[1]
            s2 = col[2]
            # print "\ns0\n",s0,"\ns1\n",s1,"\ns2\n",s2,
            try:
                date = year + "-" + month + "-" + s0.find('p',{'class':'date_num'}).text#.encode("utf-8")
                # print "date", date
            except:
                None
            try:
                title = ""
                title = s1.find('p',{'class':'title'}).text#.encode("utf-8")
                # print "title s1", title
            except:
                None
            try:
                subtitle = ""
                subtitle = s1.find('p',{'class':'subtitel'}).text#.encode("utf-8")
                # print "subtitle s1", subtitle
            except:
                None
            try:
                time = ""
                etime = ""
                ttime = ""
                ttime = s1.find('p',{'class':'time'}).text#.encode("utf-8")
                ttime = ttime.replace("Uhr","").replace(" ","").replace(".",":").split("-")
                time = ttime[0]
                try:
                    etime = ttime[1]
                except:
                    None
            except:
                None
            try:
                ref = ""
                ref = s1.find('a', href=True)["href"]
                # print "ref", ref
            except:
                None
            try:
                text = ""
                text = s1.find('p',{'class':'text'}).text#.encode("utf-8")
                # print "text", text
            except:
                None
            try:
                place = "Deutsches Theater"
                imgs = s1.findAll('img')# ,{'alt':'top'})  #.text.encode("utf-8")
                for img in imgs:
                    if img["alt"] == "top":
                        place += " - " + img["src"].split("/")[-1].replace(".jpg","")
            except:
                None
            
            if title != "":
                cont = {"date" : date, "time" : time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : ref, "place" : place}
                ret = { str(date) + "_" + time +  "_" + place.replace(" ","") : cont }
                # print "ret",ret

                curr_events[str(date) + "_" + time +  "_" + place.replace(" ","")] = cont
        return curr_events

##########################
if __name__ == '__main__':
    evt = events()
    print evt.current_events

    
