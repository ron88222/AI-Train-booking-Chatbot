import tkinter
from tkinter.scrolledtext import ScrolledText
import NLP as nlp
import knowledgeengine as ke
import knn
import csv
import webScraper
import webbrowser
import re
import sys


global qno
qno = 0
global ans
ans = ["","","","",""]
name = []
code = []
stationsDict = {}

def resetfacts():
    with open("facts.csv",'w') as file:
        file.write("null,null,null,null,null,Sorry! I didnt quite catch that. Can you say that again?")

def readfacts():
    facts = []
    with open("facts.csv", "r") as csvfile:
        csv_reader = csv.reader(csvfile,delimiter=',')
        for fact in csv_reader:
            facts=fact
    return facts

resetfacts()

with open("listStations.csv") as file:
        csv_reader = csv.reader(file,delimiter=',')
        line_count = 0
        for line in csv_reader:
                if line_count != 0:
                        name.append(line[0])
                        code.append(line[2])
                        stationsDict[line[0]] = line[2]
                line_count+=1
stations = [name,code]
#class UI():
def openLink(event):
    link = label_link.cget("text")
    webbrowser.open(link, new=2)
    
#disallows user to input during bot turn
def turntimer(userturn):
    if userturn:
        entry_user.configure(state="normal")
        button_submit.configure(state="normal")
    else:
        entry_user.configure(state="disabled")
        button_submit.configure(state="disabled")
        
#adding usertext to textlog
def usersubmit():
    usertext = entry_user.get() #get usertext 
    if usertext=="": #if user entry is empty do nothing
        return

    text_log.configure(state="normal") #unlock textlog
    text_log.insert("end", "   YOU:    "+usertext+"\n") #add usertext to the end
    text_log.configure(state="disabled") #lock textlog
    text_log.see(tkinter.END) #scroll to bottom
    
    entry_user.delete(0,tkinter.END) #delete usertext 0-END
    turntimer(False) #pass turn to bot
    bot_response(usertext)#send text to bot
    
    # hlink = "nationalrail.co.uk"
    # link = tkinter.Label(text_log, text="nationalrail.co.uk", fg="blue", cursor="hand2")
    # label_link.configure(text=hlink, fg="blue", cursor="hand2")
    # label_link.bind("<Button-1>", openLink)


def get_response(usertext):
    global qno
    global ans
    if qno == 5:
       resetfacts()
       qno = 0
       ans = ["","","","",""]
       ke.startKE("reset","","","","")
    response = process_message(usertext)
   
    
    return response

def bot_response(usertext):
    bottext = get_response(usertext)
    text_log.configure(state="normal") #unlock textlog
    text_log.insert("end", "Steven:    "+bottext+"\n") #add bottext to the end
    text_log.configure(state="disabled") #locktextlog
    turntimer(True) #pass turn to user



def process_message(msg):
    msg = msg.lower()
    global qno
    global ans
    #NLTK functions
    hlink = "nationalrail.co.uk"
    label_link.configure(text=hlink, fg="blue", cursor="hand2")
    label_link.bind("<Button-1>", openLink)
    
    hiList = ["hello","hi","hey","heya","hiya","hai","howdy","ciao","ni hao"]
    biList = ["goodbye","bye","bi","exit","see you","cya","see ya","byebye","ciao","bye bye"]
    if msg.lower() in hiList:
        return "Hello to you too user!"
    elif msg.lower() in biList:
        sys.exit()
    if msg.lower() == "good":
        return "That's very good"
    
    delayList = ["delay", "late", "delayed"]
    print(qno)
    k = False
    for w in delayList:
        if msg in delayList: 
            k = True
                
    if k == True:
        if qno == 0 or qno > 4 and qno < 10:
            qno = 10
            qno += 1
            print()
            return "How long has your train been delayed by?"
    
    if qno == 11:
        msg = re.sub(r'[^\d]',"",msg)
        msg = int(msg)
        ans[0] = msg
        qno += 1
        return "Where did your train depart from and arriving at?"
    elif qno == 12:
        x = nlp.findStation(msg)
        ke.startKE(x[1],x[0],"","","")
        facts = readfacts()
        if facts[0] != "null":
            qno += 1
            
            for s in stations:
                if x[1] == s[0]:
                    x[1] = s[1]
                if x[0] == s[0]:
                    x[0] = s[1]
            ans[1] = x[1]
            ans[2] = x[0]
        return "What time did you depart?"
    elif qno == 13:
        x = nlp.findTime(msg)
        x = re.sub(r'[^\d]',"",x)
        ans[3] = int(x)
        qno += 1
        return "What was you orginal estimated arrival?"
    elif qno == 14:
        x = nlp.findTime(msg)
        x = re.sub(r'[^\d]',"",x)
        ans[4] = int(x)
        qno += 1
        return "OK 1 sec!"
    elif qno == 15:
        s1 = " ".join(ans[1])
        s2 = " ".join(ans[2])
        x = knn.main(ans[4],ans[3],stationsDict[s1],stationsDict[s2],ans[0])
        x = "The estimated time of arrival is  "+ x
        resetfacts()
        qno = 0
        return x
        
        
    if qno == 0:
        
        x = nlp.findStation(msg)
        facts = readfacts()
        print(facts)
        print("asdaf")
        ke.startKE(x[1],x[0],"","","")
        facts = readfacts()
        print(facts)
        if facts[0] != "null":
            qno += 1
            ans[0] = x[1]
        if facts[1] != "null":
            qno += 1
            ans[1] = x[0]
        return facts[5]
    elif qno == 1:
        x = nlp.finddplace(msg)
        facts = readfacts()
        ke.startKE(x,ans[0],"","","")
        facts = readfacts()
        if facts[0] != "null":
            qno += 1
            ans[0] = x
        return facts[5]
    elif qno == 2:
        x = nlp.findDate(msg)
        ke.startKE(ans[0],ans[1],"",x,"")
        facts = readfacts()
        if facts[2] != "null":
            qno += 1
            ans[2] = x
        return facts[5]
    elif qno == 3:
        x = nlp.findTime(msg)
        ke.startKE(ans[0],ans[1],x,ans[2],"")
        facts = readfacts()
        if facts[3] != "null":
            qno += 1
            ans[3] = x
        return facts[5]
    elif qno == 4:
        x = nlp.checkDepart(msg)
        ke.startKE(ans[0],ans[1],ans[3],ans[2],x)
        facts = readfacts()
        if facts[4] != "null":
            qno += 1
            ans[4] = x
            temp =  webScraper.main()
            hlink = temp[1]
            label_link.configure(text=hlink, fg="blue", cursor="hand2")
            return temp[0]
        return["arrival or departure?"]
        
    if msg == " ":
        return "Hello?"
    
    facts = readfacts()
    print(facts)
    
    
    # while "null" in facts:
        #ke.test(msg)
        # print("NUL IN FACT")
        
    return "Sorry! I don't understand!"

# def resetfacts():
    # with open("facts.csv",'w') as file:
        # file.write("null,null,null,null,null,Sorry! I didnt quite catch that. Can you say that again?")

# def readfacts():
    # facts = []
    # with open("facts.csv", "r") as csvfile:
        # csv_reader = csv.reader(csvfile,delimiter=',')
        # for fact in csv_reader:
            # facts=fact
    # return facts
    

#function for when enter is pressed
def func(event):
    usersubmit()

    #def __init__(self):
#window
window = tkinter.Tk()
window.geometry("550x500")
window.title("ChatBotSteven2.0")
window.grid_propagate(False)
window.grid_rowconfigure(0,weight=1)
window.grid_columnconfigure(0,weight=1)

window.bind('<Return>', func) #enter calls func

#welcomelabel
label_welcome = tkinter.Label(window, text="Welcome, I'm Steve!")
label_welcome.grid(column=0, row=0)

#LinkLabel
label_link = tkinter.Label(window, text="nationalrail.co.uk", fg="blue", cursor="hand2")
label_link.grid(column=0, row=1,)
label_link.bind("<Button-1>", openLink)

#textlog
text_log = ScrolledText(window, width=50, height=25, state="normal")
text_log.insert("end", "Steven:    Hi, I'm Steve! I can help you book tickets! Where would you like to go?\n")
text_log.configure(state="disabled")
text_log.grid(column=0, row=2)


#userentry
entry_user = tkinter.Entry(window, width=52)
entry_user.grid(column=0, row=3, padx=(0,100))

#submitbutton
button_submit = tkinter.Button(window, text="Submit", command=usersubmit)
button_submit.grid(column=0, row=3, padx=(300,0))


window.mainloop()



#def main():
 #   ui = UI()
    
    

#if __name__ == '__main__':
#    main()
