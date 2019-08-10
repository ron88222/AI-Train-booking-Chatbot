from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
import nltk
import re

#find destination 
def findaplace(usertext):
        usertext = re.sub(r'[\.!\?,]',"",usertext) #remove useless character
        visit_word_list = ["To","Go","Going","Visit","Visiting","Arrive","Arriving"] #list for all visiting words
        userWords = word_tokenize(usertext) #split the sentence into words
        capWords = []
        for i in userWords: #Capitalize the first letter 
            capWords.append(i.capitalize())
        taggedWords = pos_tag(capWords) # get the tags
        aplace = []
        tupleToList = list(taggedWords[0]) # tuple convert to list
        #print(taggedWords)
        if tupleToList[1] == "NNP" or tupleToList[1] == "NN" or tupleToList[1] == "RB": # extracted all the wanted information
                if len(capWords) == 1:# station name which has one word
                    aplace.append(tupleToList[0])
        else: # for station which has more than a word
                pos = 0
                n=0
                for w in capWords:
                    if w in visit_word_list:
                        pos = n
                    n+=1
                n=1
                while n + pos < len(capWords):
                    aplace.append(capWords[pos+n])
                    n+=1 
        print(aplace)
        return aplace

#find departure
def finddplace(usertext):
        usertext = re.sub(r'[\.!\?,]',"",usertext) #remove useless character
        from_word_list = ["From","Leave","Leaving","At"]#list for all departing words
        userWords = word_tokenize(usertext)#split the sentence into words
        capWords = []
        for i in userWords:#Capitalize the first letter
            capWords.append(i.capitalize())
        taggedWords = pos_tag(capWords)# get the tags
        dplace = []
        tupleToList = list(taggedWords[0])# tuple convert to list
        #print(taggedWords)
        if tupleToList[1] == "NNP" or tupleToList[1] == "NN" or tupleToList[1] == "RB":# extracted all the wanted information
                if len(capWords) == 1:# station name which has one word
                    dplace.append(tupleToList[0])
        else:# for station which has more than a word
                pos = 0
                n=0
                for w in capWords:
                    if w in from_word_list:
                        pos = n
                    n+=1
                n=1
                while n + pos < len(capWords):
                    dplace.append(capWords[pos+n])
                    n+=1 
        print(dplace)
        return dplace

#find both arrival and departure stations       
def findStation(usertext):
    usertext = re.sub(r'[\.!\?,]',"",usertext)#remove useless character
    visit_word_list = ["To","Go","Going","Visit","Visiting","Arrive","Arriving"]#list for all arriving words
    from_word_list = ["From","Leave","Leaving","At"]#list for all departing words
    userWords = word_tokenize(usertext)#split the sentence into words
    capWords = []
    for i in userWords:#Capitalize the first letter
        capWords.append(i.capitalize())
    #print(capWords)        
    taggedWords = pos_tag(capWords)# get the tags
    dplace = []
    aplace = []
    tupleToList = list(taggedWords[0])# tuple convert to list
    if tupleToList[1] == "NNP" or tupleToList[1] == "NN" or tupleToList[1] == "RB":# extracted all the wanted information
            if len(capWords) == 1: #only one station extracted, set it as arrival station
                aplace.append(tupleToList[0])
            else: # two stations extracted
                identifierpos = 0
                n=0
                itype = 'n' 
                for w in capWords:# check for arrival or departure
                    if w in visit_word_list:
                        identifierpos = n
                        itype = 'v'
                    elif w in from_word_list:
                        identifierpos = n
                        itype = 'f'
                    n+=1
                if itype == 'v': #if it is arrival
                    n=1
                    while n + identifierpos < len(capWords):
                        aplace.append(capWords[identifierpos+n])
                        n+=1
                    if n > 0:
                        n=1
                        while identifierpos-n >= 0:
                            dplace.insert(0,capWords[identifierpos-n])
                            n+=1
                elif itype == 'f': # if it is departure
                    n=1
                    while n + identifierpos < len(capWords):
                        dplace.append(capWords[identifierpos+n])
                        n+=1
                    if n > 0:
                        n=1
                        while identifierpos-n >= 0:
                            aplace.insert(0,capWords[identifierpos-n])
                            n+=1
                
    else:
            n = 0
            while n < len(taggedWords):
                    tupleToList = list(taggedWords[n])
                    if n!= len(taggedWords)-1:
                            nextElement = list(taggedWords[n+1])
                            currentIndex = n+1
                    n += 1
                    
                    if tupleToList[0] in visit_word_list and nextElement[1] == "NNP":
                            aplace.append(nextElement[0])
                            currentIndex += 1
                            while currentIndex < len(taggedWords):
                                    temp = []
                                    temp = (list(taggedWords[currentIndex]))
                                    if temp[1] == "NNP" and capWords[currentIndex] not in from_word_list:
                                        aplace.append(capWords[currentIndex])
                                    else:
                                        currentIndex = len(taggedWords)
                                    currentIndex += 1
                                    
                    elif tupleToList[0] in from_word_list and nextElement[1] == "NNP":
                            dplace.append(nextElement[0])
                            currentIndex += 1
                            while currentIndex < len(taggedWords):
                                    temp = []
                                    temp = (list(taggedWords[currentIndex]))
                                    if temp[1] == "NNP" and capWords[currentIndex] not in visit_word_list:
                                        dplace.append(capWords[currentIndex])
                                    else:
                                        currentIndex = len(taggedWords)
                                    currentIndex += 1
    return aplace,dplace

##########################################################################################################################
#find time
def findTime(usertext):
    userWords = word_tokenize(usertext)#remove useless character
    morning_list = ["am","a.m","morning","noon"] #list for morning words
    afternoon_list = ["pm","p.m","afternoon","evening","night","midnight"]#list for afternoon words
    ct = ""
    for j in userWords: #check morning or afternoon
        if j in morning_list:
            ct = "m"
        elif j in afternoon_list:
            ct = "a"
    taggedWords = pos_tag(userWords) #get tags
    tupleToList = list(taggedWords) # convert tuple to list
    n = 0
    d = ""
    time = []
    lis=""
    ck = ""
    while n < len(tupleToList):
        temp = tupleToList[n]
        isd = temp[0].isdigit()
        if not isd and temp[1] == "CD": 
            ck = str(temp[0])
            for z in ck:
                if not z.isdigit():
                    lis += z
            lis = lis.replace(":","")
            if lis in morning_list:
                ct = "m"
                ck = ck.replace(lis,"")
                tupleToList = list(pos_tag(word_tokenize(ck)))
                temp = tupleToList[0]
            elif lis in afternoon_list:
                ct = "a"
                ck = ck.replace(lis,"")
                tupleToList = list(pos_tag(word_tokenize(ck)))
                temp = tupleToList[0]
        if ":" in temp[0] and temp[1] == "CD":
            t = (re.findall(r'\d+', temp[0]))
            for i in t:
                d += i
            if len(d) == 4:
                hour = d[0]+d[1]
                mins = d[2]+d[3]
                if int(d) < 1159 and ct == "a":
                    d = str(int(hour) + 12)
                    time = d+mins
                elif int(hour) == 12:
                    if ct == "a" or ct == "":
                        time = hour+mins
                    elif ct == "m":
                        time = "00"+mins
                elif int(hour) > 12 or ct == "":
                    time = d
            elif len(d) == 3 and (ct == "m" or ct == ""):
                    time = "0"+d
            elif len(d) == 3 and ct == "a":
                d = str(int(d) + 1200)
                time = d
        elif temp[1] == "CD":
            if len(temp[0]) == 2:
                if ct == "m" or ct == "":
                    if int(temp[0]) != 12:
                        d = temp[0]+"00"
                        time = d
                        print("adverb")
                    else:
                        time = "0000"
                        print("vvs")
                else:
                    d = str(int(temp[0]+"00")+1200)
                    time = d
            elif len(temp[0]) == 1: #length is 1 e.g. 9
                if ct == "m" or ct == "": #in morning or not mentioned
                    d = "0"+temp[0]+"00"
                    time = d
                else: #it is afternoon
                    d = str(int(temp[0]+"00")+1200)
                    time = d
            elif len(temp[0]) == 3 and (ct == "m" or ct == ""):
                time = "0"+temp[0]
            elif len(temp[0]) == 3 and ct == "a":
                d = str(int(temp[0]) + 1200)
                time = d
            elif len(temp[0]) == 4:
                d = temp[0]
                hour = d[0]+d[1]
                mins = d[2]+d[3]
                if int(d) < 1159 and ct == "a":
                    d = str(int(hour) + 12)
                    time = d+mins
                elif int(hour) == 12:
                    if ct == "a" or ct == "":
                        time = hour+mins
                    elif ct == "m":
                        time = "00"+mins
                elif int(hour) > 12 or ct == "":
                    time = d
        elif temp[0] == "noon": #noon = 1200
            time = "1200"
        elif temp[0] == "midnight": #midnight = 0000
            time = "0000"
        n += 1
    if time == "2400": #2400 = 0000
        time = "0000"
    print("time : ", time)
    return time

##########################################################################################################################
#find date
def findDate(usertext):
    usertext = re.sub(r'(?<!\d)\.(?!\d)', '', usertext) # remove unwanted characters
    userWords = word_tokenize(usertext) #split the sentence into words
    capWords = []
    day = []
    month = []
    year = []
    check = []
    for i in userWords: #capitalize the first letter in each words
            capWords.append(i.capitalize())
    taggedWords = pos_tag(capWords) # get the tags
    tupleToList = []
    for n in taggedWords: # convert tuple to list
        tupleToList.append(list(n))
    getAllData = []
    temp = []
    getDay = ""
    getMonth = ""
    getYear = ""
    for each in tupleToList: # word type for month
        if each[1] == "NNP" or each[1] == "NN" or each[1] == "JJ":
            month.append(each[0])
        elif each[1] == "CD": # digit and word type
            check.append(each[0])
    for date in check: #extract information 
        if '/' in date: # day/month/year format
            n = 0
            while date[n] != "/": #extract day
                getDay = getDay + str(date[n])
                n += 1
            day.append(getDay)
            n += 1
            while n < len(date) and date[n] != "/": #extract month
                getMonth = getMonth + str(date[n])
                n += 1
            month.append(getMonth)
            n += 1
            while n < len(date): # extract year
                getYear = getYear + str(date[n])
                n += 1
            year.append(getYear)
            if day[0][0] != "0": #if first digit in day not 0 and smaller than 10, add a 0 in front
                if int(day[0]) < 10:
                    day[0] = "0"+day[0]
            if month[0][0] != "0":#if first digit in month not 0 and smaller than 10, add a 0 in front
                if int(month[0]) < 10:
                    month[0] = "0"+month[0]
        else:
            temp.append(date)

    if len(temp) < 4 and len(temp) > 1: # 23rd march 2019 format
        d = re.findall(r'\d+',temp[0]) # extract day
        y = re.findall(r'\d+',temp[1]) # extract year
        day = d
        if day[0][0] != "0":#if first digit in day not 0 and smaller than 10, add a 0 in front
                if int(day[0]) < 10:
                    day[0] = "0"+day[0]
        year = y
    elif len(temp) == 1: #if first digit in day not 0 and smaller than 10, add a 0 in front
        d = re.findall(r'\d+',temp[0])
        day = d
        if day[0][0] != "0":
                if int(day[0]) < 10:
                    day[0] = "0"+day[0]
    if not month: #no month extracted, set it as nothing
        month.append("")
    if not year:#no year extracted, set it as nothing
        year.append("")
    mergeList = day + month + year #merge the lists to suit the format
    print("merge:",mergeList)
    return mergeList
	
##########################################################################################################################
#find arrival or departure
def checkDepart(usertext):
    usertext = re.sub(r'(?<!\d)\.(?!\d)', '', usertext) #remove useless characters
    userWords = word_tokenize(usertext) #split the sentence into words
    answer = ""
    capWords = []
    for i in userWords: #capitalize each words
            capWords.append(i.capitalize())
    taggedWords = pos_tag(capWords) #get the tags
    tupleToList = []
    for n in taggedWords: #convert tuple to list
        tupleToList.append(list(n))
    for each in tupleToList: #extract useful information
        if each[1] == "NN" or each[1] == "JJ":
            answer = each[0]
    print(answer)
    return answer

#findaplace("from london liverpool street")