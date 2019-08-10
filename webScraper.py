from bs4 import BeautifulSoup
import urllib.request
import re
import csv


def request_page(dStation, aStation, date, time, when):
    #Request page
    dStation = dStation.replace(" ","")
    aStation = aStation.replace(" ","")
    url = "http://ojp.nationalrail.co.uk/service/timesandfares/"+dStation+"/"+aStation+"/"+date+"/"+time+"/"+when
    page = urllib.request.urlopen(url)

    #retreive html from page
    parsedHTML = BeautifulSoup(page, "html.parser")
    return parsedHTML, url
    

def get_tickets_info(content):

    #Find cheapest price
    cheapestPrice = str(content.findAll("strong", {"class": "ctf-pr"}))
    cheapestPrice = re.sub(r"<.*?>", "", cheapestPrice) 
    print("Fares From: ",cheapestPrice)

    #Find all tables rows
    tableRow = content.findAll("tr")
    ticketList = [] # list of avalible tickets

    for row in tableRow:
        r = str(row)
        if "mtx" in r: #from all mtx table rows
            r = resub_stuff(r) #remove unnecessary tags

            ticket = [] #all ticket data
            datanames = ["dep","from","to","arr","dur","chg","fare"] #all td class names
            
            for name in datanames: #for each data class
                if name != "fare":
                    pattern = r'<tdclass=\"'+name+'\">(.*?)</td' #remove td tag
                else:
                    pattern = r'(£\d*\.\d\d)' #if price only select price
                result = re.findall(pattern, r)
                if name == "chg" and result==[]: #if no change default to 0
                    result = ['0']
                ticket.append(result[0]) #add ticket data into ticket 
            ticketList.append(ticket) #add ticket into ticket list

    return ticketList
        

def resub_stuff(r):
    r = re.sub(r'\s*','',r)                 #remove space
    r = re.sub(r'(<(a|/a).*?>)','',r)       #remove all tage beginning with a
    r = re.sub(r'(<div.*?>|</div>)','',r)   #remove all div tags
    r = re.sub(r'(<span.*?>|</span>)','',r) #remove all span tags
    r = re.sub(r'(<img.*?/>)','',r)         #remove all img tags

    return r

#def print_tickets(x):
#    for a in x:
#        print(a)

def showToUI(msg,url):
    leavingTime = msg[0]
    dplace = msg[1]
    aplace = msg[2]
    arrivalTime = msg[3]
    duration = msg[4]
    change = msg[5]
    price = msg[6]
    Information = "|" + "Leaving time: " + leavingTime + "|\n" + "|" + "Departure from: " + dplace + "|\n" + "|" +"Arriving at: " +  aplace + "|\n" + "|" + "Arriving time: " + arrivalTime + "|\n" + "|" + "Duration: " + duration + "|\n" + "|" + "Change: " + change + "|\n" + "|" + "Price: " + price + "|\n" + "Link: " + url + "\n" 
    print(Information)
    return(Information ,url)
    
def readfacts():
    facts = []
    with open("facts.csv", "r") as csvfile:
        csv_reader = csv.reader(csvfile,delimiter=',')
        for fact in csv_reader:
            facts=fact
    return facts
    
def main():
    fact = readfacts()
    #query varibles
    dStation = fact[0]
    aStation = fact[1]
    tempDate = fact[2].split('-')
    tempDate.reverse()
    date = tempDate[0]+tempDate[1]+tempDate[2]
    print(date)
    tempTime = re.sub(r':',"",fact[3])
    time = tempTime[:4]
    when = fact[4]
    page_contents = request_page(dStation, aStation, date, time, when)
    url = page_contents[1]
    page_contents = page_contents[0]
    ticketList = get_tickets_info(page_contents)
    #print(ticketList[0])
    n=0
    cheapestTicket = [] 
    cheapestPrice = 0
    for ticket in ticketList:
        price = ticket[6]
        price = int(re.sub(r'[^\d]',"",price))
        if price < cheapestPrice or cheapestPrice == 0:
            cheapestPrice = price            
            cheapestTicket = ticketList[n]
        n+=1
    #print(firstRow[0])
    trainInformation = showToUI(cheapestTicket,url)
    return trainInformation
	
if __name__ == '__main__':
   main()
