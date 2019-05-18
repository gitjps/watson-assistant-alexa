#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.

#
# @return The output of this action, which must be a JSON object.
#
#
# import bs4
from urllib.request import urlopen as myReq
from bs4 import BeautifulSoup as mySoup
import json

def main(dict):

    myUrl = 'https://www.berlin.de/polizei/polizeimeldungen/'
    myClient = myReq(myUrl)
    pageHtml = myClient.read()
    myClient.close()
    pageSoup = mySoup(pageHtml, "html.parser")
    rows = pageSoup.findAll("li",{"class":"row-fluid"})
    r = []
    for x in rows:
        time = x.findAll("div", {"class":"span2"})
        time0 = time[0].text
        a = x.findAll("a", {})
        message_link = "https://www.berlin.de" + a[0].get('href')
        message_text = a[0].text
        span10 = x.findAll("div", {"class":"span10"})
        cat = span10[0].findAll("span",{"class":"category"})
        if len(cat) > 0:
            cat[0].strong.replace_with("")
            district = cat[0].text
            if district == dict["district"]:
                return {
                    "text" : "Die letzte Meldung ist vom " + time0 + ". Der Titel der Meldung ist : " + message_text,
                    "police_message_link" : message_link
                }
            else:
                span10 = span10
    
    return {
        "text" : "Es liegen keine Meldungen für den Stadtbezirk " + dict["district"] + " vor"
    }
