import sys
from datetime import date, datetime, timedelta

PostDir="/home/uschwar1/ownCloud/AC/html/hugo/test-site-goest/content/post/"

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
    print ("Titel")
    title =  sys.stdin.readline()[:-1]
    print ("Untertitel")
    subtitle =  sys.stdin.readline()[:-1]
    print ("Text")
    text = ""
    for line in sys.stdin.readlines():
        text += line
    print ("URL f. weitere Informationen")
    url =  sys.stdin.readline()[:-1]
    print ("author")
    author =  sys.stdin.readline()[:-1]
    
    
    cont = {"date" : Date, "time" : Time, "title" : title, "subtitle" : subtitle, "text" : text, "url4infos" : url, "author" : author}
    curr_posts = {}
    curr_posts[str(Date) + "-" + Time.replace(":","-") +  "-" + title.replace(" ","").replace(",","").replace(":","").replace(";","").replace("[","").replace("]","")  +  "-" + author.replace(" ","")] = cont
    return curr_posts

def get_publish_date(date_str, publish_delta):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    publish_date = date - timedelta(days=publish_delta)
    return publish_date.strftime("%Y-%m-%d")



##########################
if __name__ == '__main__':
    evt = get_event()
    # print (evt)

    for event in evt:
        Evt = evt[event]

    try:
        LocURL = locURL[Evt["organizer"]][0]
        LocIcon = locURL[Evt["organizer"]][1]
    except:
        LocURL = ""
        LocIcon = "goest-icon.png"

    fo = open(PostDir + event + ".md", "w")
    fo.write("---"+ "\n")
    fo.write("layout:        events"+ "\n")
    fo.write("title:         \"" + Evt["title"] + "\""+ "\n")
    fo.write("subtitle:      \"" + Evt["subtitle"] + "\""+ "\n")
    fo.write("date:          " + Evt["date"] + "T" + Evt["time"] + ":00+01:00"+ "\n")
    fo.write("publishdate:   " + get_publish_date(Evt["date"],0) + "T00:00:00+01:00"+ "\n")
    fo.write("author:        \"" + Evt["author"] + "\""+ "\n")
    fo.write("---"+ "\n")
    fo.write(""+ "\n")
    fo.write(Evt["title"]+ "\n")
    fo.write("==========="+ "\n")
    fo.write(""+ "\n")
    fo.write(Evt["subtitle"]+ "\n")
    fo.write("-----------"+ "\n")
    fo.write(""+ "\n")
    fo.write(Evt["text"])
    fo.write(""+ "\n")
    if Evt["url4infos"] != "":
        fo.write("[Weitere Informationen...](" + Evt["url4infos"] + ")"+ "\n")
    fo.close()
