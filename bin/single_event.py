import sys
from datetime import date, datetime, timedelta


locURL = {
    "Lumiere" : ["http://www.lumiere.de/","lumiere-icon.png"],
    "ThOP" : ["http://www.thop.uni-goettingen.de/","thop-uni-goettingen-icon.png"],
    "Literarisches Zentrum" : ["http://www.literarisches-zentrum-goettingen.de/","literarisches-zentrum-icon.png"],
    "Junges Theater" : ["http://junges-theater.de/","junges-theater-icon.png"],
    "Deutsches Theater" : ["https://www.dt-goettingen.de/","deutsches-theater-icon.png"],
    "EXIL" : ["http://www.exil-web.de/","Exil-live-music-club.png"]
    }

    
    
def get_event():
    today = datetime.now().strftime('%Y-%m-%d')
    print ("Datum (" + today + ")")
    Date = sys.stdin.readline()[:-1]
    if Date == "":
        Date = today
    now = datetime.now().strftime('%H:%M')
    print ("Uhrzeit (" + now + ")" )
    Time =  sys.stdin.readline()[:-1]
    if Time == "":
        Time = now
    print ("Uhrzeit Ende (" + now + ")" )
    etime =  sys.stdin.readline()[:-1]
    print ("Titel")
    title =  sys.stdin.readline()[:-1]
    print ("Untertitel")
    subtitle =  sys.stdin.readline()[:-1]
    print ("Text")
    text = ""
    for line in sys.stdin.readlines():
        text += line
    print ("URL")
    url =  sys.stdin.readline()[:-1]
    print ("Ort")
    place =  sys.stdin.readline()[:-1]
    print ("Organisator")
    organizer =  sys.stdin.readline()[:-1]
    
    
    cont = {"date" : Date, "time" : Time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : url, "place" : place, "organizer" : organizer}
    curr_events = {}
    curr_events[str(Date) + "_" + Time +  "_" + place.replace(" ","").replace(",","")] = cont
    return curr_events

def get_publish_date(date_str, publish_delta):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    publish_date = date - timedelta(days=publish_delta)
    return publish_date.strftime("%Y-%m-%d")



##########################
if __name__ == '__main__':
    evt = get_event()
    print (evt)

    print ()
    for event in evt:
        Evt = evt[event]

    try:
        LocURL = locURL[Evt["organizer"]][0]
        LocIcon = locURL[Evt["organizer"]][1]
    except:
        LocURL = ""
        LocIcon = "goest-icon.png"

    print (LocURL)
    print (LocIcon)
    print ("---")
    print ("layout:        events")
    print ("title:         \"" + Evt["title"] + "\"")
    print ("subtitle:      \"" + Evt["subtitle"] + "\"")
    print ("date:          " + Evt["date"] + "T" + Evt["time"] + ":00+01:00")
    print ("publishdate:   " + get_publish_date(Evt["date"],10) + "T00:00:00+01:00")
    print ("author:        \"" + Evt["organizer"] + "\"")
    print ("place:         \"" + Evt["place"] + "\"")
    print ("URL:           \"" + Evt["url"] + "\"")
    print ("image:         \"" + LocIcon + "\"")
    print ("locURL:        \"" + LocURL  + "\"")
    print ("---")
    print ("")
    print (Evt["title"])
    print ("===========")
    print ("")
    print (Evt["subtitle"])
    print ("-----------")
    print ("")
    print (Evt["text"])

