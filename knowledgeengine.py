from pyknow import *
from pyknow.utils import unfreeze
from pyknow.utils import freeze
import csv
from datetime import datetime
import NLP as nlp

currentFacts = ["null,","null,","null,","null,","null,","Sorry! I didnt quite catch that. Can you say that again?"]
var = ["","","False,","False,","False,","False,","False"]
name = []
code = []

with open("listStations.csv") as file:
        csv_reader = csv.reader(file,delimiter=',')
        line_count = 0
        for line in csv_reader:
                if line_count != 0:
                        name.append(line[0])
                        code.append(line[2])
                line_count+=1
stations = [name,code]

def updatevar(varNum, varInfo):
    with open("var.csv",'w') as file:
        if (varNum == 6):
            var[varNum] = varInfo
        else:
            var[varNum] = varInfo+","
        file.writelines(var)  

def updatefacts(factType, factInfo):
    with open("facts.csv",'w') as file:
        if (factType == 5):
            currentFacts[factType] = factInfo
        else:
            currentFacts[factType] = factInfo+","
        #print(currentFacts)
        file.writelines(currentFacts)    

#reading frozen list
def listread(l):
    temp = ""
    n = 0
    for a in unfreeze(l):
        if n < len(unfreeze(l))-1:
            temp = temp + a + " "
        else:
            temp = temp + a
        n+=1
    l = temp
    return l


class response(KnowledgeEngine):
##    @Rule(EXISTS(dStation()))
##    def allFacts(self):
##        print("DDDD")
    # @Rule(NOT(Fact(dstation=W())),salience = 9)
    # def set_var(self,list1):
        # hasds = tue
        # aS = list2[1]
        
    
    
    @Rule(NOT(Fact(dstation=W())),salience = 9)
    def req_dest(self):
        print("need dest")
        #self.declare(Query(dstation = "CAMB TEST")) #get dstation

    @Rule(NOT(Fact(astation=W())),salience = 8)
    def req_arr(self):
        print("need arr")
        #get astation

    @Rule(NOT(Fact(time=W())),salience = 7)
    def req_time(self):
        print("need time")
        #get time

    @Rule(NOT(Fact(date=W())),salience = 6)
    def req_date(self):
        print("need date")

    @Rule(NOT(Fact(when=W())),salience = 5)
    def req_time(self):
        print("need when")

    @Rule(Fact(dstation = MATCH.dstation),salience = 3)
    def print_dstation(self,dstation):
        if type(unfreeze(dstation)) is list:
            dstation = listread(dstation)
            
        if dstation == "":
            print("empty")
        elif dstation == "reset":
            updatefacts(0,"null")
            updatefacts(1,"null")
            updatefacts(2,"null")
            updatefacts(3,"null")
            updatefacts(4,"null")
            updatefacts(5,"Sorry! I didnt quite catch that. Can you say that again?")
		
        if dstation in name:
            i=name.index(dstation)
            print(dstation+ "'s code is "+ code[i])
            updatefacts(0,dstation)
            updatefacts(5,"What date would you like to go?")
            var[2] = "True"
        else:
            print("Could not find "+dstation)
            
        

    @Rule(Fact(astation = MATCH.astation),salience = 4)
    def print_astation(self,astation):
        if type(unfreeze(astation)) is list:
            astation = listread(astation)
        if astation in name:
            i=name.index(astation)
            print(astation+ "'s code is "+ code[i])
            updatefacts(1,astation)
            updatefacts(5,"Where are you leaving from?")
        else:
            print("Could not find "+astation)
            
    
    @Rule(Fact(date = MATCH.date),salience = 2)
    def print_date(self,date):
        if date == "":
            print("NO DATE")
            return
        if type(unfreeze(date)) is list:
            d=datetime.date(datetime.now())
            if date[2] == "" and date[1] == "":
                if int(date[0]) < d.day:
                    date = date[0]+" "+str(d.month + 1)+" "+str(d.year)
                else:
                    date = date[0]+" "+str(d.month)+" "+str(d.year)
                    
            elif date[2] == "" and date[1] != "":
                
                if int(date[1]) < d.month:
                    date = date[0]+" "+date[1]+" "+str(d.year + 1)
                elif int(date[1]) == d.month:
                    if int(date[0]) < d.day:
                        date = date[0]+" "+date[1]+" "+str(d.year + 1)
                else:
                    date = date[0]+" "+date[1]+" "+str(d.year)
            else:
                date = listread(date)
            
        date = datetime.strptime(date, '%d %m %Y')
        date = datetime.date(date)
        #date = datetime.date(date)
        if date > datetime.date(datetime.now()):
            updatefacts(2,str(date))
            updatefacts(5,"What time?")
        elif date == datetime.date(datetime.now()):
            updatevar(1,str(date))

            updatevar(0,"True")

    @Rule(Fact(time = MATCH.time),salience = 1)
    def print_time(self,time):
        if time == "":
            print("no time")
            return
        if type(unfreeze(time)) is list:
            time = listread(time)
        time = datetime.strptime(time, '%H%M')
        time = datetime.time(time)
        if var[0] == "True,":
            if time > datetime.time(datetime.now()):
                updatefacts(2,var[1])
                updatefacts(5,"Would you like to arrive or depart at this time?")
                #print(date)
            else:
                print("You must pick a time in the future")
        updatefacts(3,str(time))
        updatefacts(5,"Would you like to arrive or depart at this time?")
        print(time)
        
    @Rule(Fact(when = MATCH.when),salience = 0)
    def print_when(self,when):
        if type(unfreeze(when)) is list:
            when = listread(when)
            
        if when == "Arrival" or when == "Arrive":
            updatefacts(4,"arr")
            updatefacts(5,"Okay thanks! Please hold on while we process your request")
        elif when == "Departure" or when == "Depart":
            updatefacts(4,"dep")
            updatefacts(5,"Okay thanks! Please hold on while we process your request")
        print(when)
        
    
##    @Rule(AND(dStation(True), aStation(True), Time(True), Date(True), When(True)) )
##    def allFacts(self):
##        print("All Facts Aquired")
##
##    @Rule(AND(dStation(False), aStation(False), Time(False), Date(False), When(False)) )
##    def allFalse(self):
##        print("All Missing")
##
##    @Rule(AND(dStation(True), aStation(False), Time(False), Date(False), When(False)) )
##    def dest(self):
##        print("Where would you like to go?")
##
##    @Rule(AND(dStation(False), aStation(True), Time(False), Date(False), When(False)) )
##    def dest(self):
##        print("Where will you be departing from?")
##        
##    @Rule(AND(dStation(True), aStation(True), Time(False), Date(False), When(False)) )
##    def bothStations(self):
##        print("When would you like to Leave or Arrive") 

def startKE(dS, aS, t, d, w):
    engine=response()
    engine.reset()
    currentFacts = ["null,","null,","null,","null,","null,","Sorry! I didnt quite catch that. Can you say that again?"]
    # facts = NLP(msg)
    
    #testdata       
    #dS = "Cambridge"
    ##aS = True
    ##t = True
    ##d = True
    ##w = True
    ##
    ##engine.declare((dStation(dS)),(aStation(aS)),(Time(t)),(Date(d)),(When(w)) )
    

    # dS = deststa
    # aS = arrsta
    # t = tim
    # d = dat
    # w = whe
    st= "dstation = dS, astation = aS, time = t, date = d, when = w"
    engine.declare(Fact(dstation = dS, astation = aS, time = t, date = d, when = w)) 
    

    #engine.declare((dStation(dstation = dS)),(aStation(astation = aS)),(Time(time = t)),(Date(date = d)),(When(when = w)) )
    engine.run()


#startKE("Cambridge","","","","Arrive")
#yeild  somthingngngngn