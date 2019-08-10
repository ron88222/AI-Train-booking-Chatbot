import csv
import datetime


def importCSV(filename):
    data = []
    with open(filename, "r") as file:
        csv_reader = csv.reader(file,delimiter=',')
        for a in csv_reader:
                data.append(a)
    return data


def sortList(data):

    trains = [] 
    n=1
    while n<len(data[0]):
        train = []
        m=0
        while m<len(data):
            loc = data[m][0]
            pta = data[m][n]
            ta = data[m][n+1]
            ptd = data[m][n+2]
            deL = data[m][n+3]
            train.append([loc,pta,ta,ptd,deL])
            m=m+1
        n=n+4
        trains.append(train)

    return trains

def lowest3(distList):
    min1=9999999
    min2=9999999
    min3=9999999
    min11=0
    min22=0
    min33=0
    n=0
    while n<len(distList):
        if distList[n][0]<min3:
            tmp = min3
            tmp1 = min33
            min3 = distList[n][0]
            min33 = distList[n][1]
            if min3<min2:
                tmp = min2
                tmp1 = min22
                min2 = min3
                min22 = min33
                min3 = tmp
                min33 = tmp1
                if min2<min1:
                    tmp = min1
                    tmp1 = min11
                    min1 = min2
                    min11 = min22
                    min2 = tmp
                    min22 = tmp1
        n=n+1
    return [min11,min22,min33]

def convertTotalMinutes(time):
    if len(str(time))==3:
        time = "0"+str(time)
    h = str(time)[0:2]
    m = str(time)[2:4]
    totalMinutes = int(h)*60 + int(m)

    return totalMinutes #Int


def TotalMinutesToTime(total):
    x = str(datetime.timedelta(minutes=total))[:-3]
    return x

# def removeColonTime(time):
#     x = str(time)[]

# Pass in (fromStation, toStation, currStation, delay) into the 'main' paramenters
def main(dTime,aTime,fStation,tStation,d):
    print("Hi")

    # timenow = datetime.datetime.now().time()
    # timebefore = datetime.datetime.now() - datetime.timedelta(minutes=10)
    # timelater = datetime.datetime.now() + datetime.timedelta(minutes=10)
    # print("NOW:",timenow,"BEFORE", timebefore,"LATER", timelater)


    ### Facts
    depTIME = convertTotalMinutes(dTime)
    depTIME = TotalMinutesToTime(depTIME).replace(":","")
    arrTIME = convertTotalMinutes(aTime)
    arrTIME = TotalMinutesToTime(arrTIME).replace(":","")
    fromStation = fStation.replace(" ","")
    toStation = tStation.replace(" ","")
    delay = int(d)

    # depTIME = convertTotalMinutes(depTIME)
    # depTIME = TotalMinutesToTime(depTIME).replace(":","")
    # arrTIME = convertTotalMinutes(arrTIME)
    # arrTIME = TotalMinutesToTime(arrTIME).replace(":","")

    # print(dTime,aTime,fStation,tStation,d)
    # print(type(dTime),type(aTime),type(fStation),type(tStation),type(d))
    # print(depTIME,arrTIME,fromStation,toStation,delay)

    ### Facts
    # depTIME = 1000
    # arrTIME = 1200
    # fromStation = "DIS"
    # toStation = "CHM"
    # # currStation = "IPS"
    # delay = 15
    
    ### Import CSV data
    
    filename = "NRWLST.csv"
    data = importCSV(filename)

    ### Get ID of routes without required stations

    # print("Removing routes")
    removeIDlist = []
    z=0
    #a is each station
    for a in data:
        if fromStation==a[0] or toStation==a[0]:
            # print(fromStation,a[0],"|",toStation,)
            n=0
            while n<len(a):
                if(fromStation==a[0]):
                    #Check departure times
                    if n==0:
                        n=n+3
                        continue
                    if a[n]=="":
                        # print("Something empty")
                        if n not in removeIDlist:
                            removeIDlist.append(n)
                            removeIDlist.append(n+1)
                            removeIDlist.append(n-1)
                            removeIDlist.append(n-2)

                if(toStation==a[0]):
                    #Check delays
                    if n==0:
                        n=n+4
                        continue

                    if a[n]=="":
                        # print("Something empty")
                        if n not in removeIDlist:
                            removeIDlist.append(n)
                            removeIDlist.append(n-1)
                            removeIDlist.append(n-2)
                            removeIDlist.append(n-3)
                n=n+4
        z=z+1

    removeIDlist.sort(reverse=True)
    
    # print(removeIDlist)

    for a in removeIDlist:
        for b in data:
            b.pop(a)

    # print("Unecessary routes removed.")

    depTimeMins = convertTotalMinutes(depTIME)
    arrTimeMins = convertTotalMinutes(arrTIME)

    trains = sortList(data)
    # print(trains)

    theList = []
    distList = []
    n=0
    for train in trains:
        # print()
        for station in train:
            # print(fromStation,station[0])
            if fromStation==station[0]:
                # print("deptime",depTIME,station[3])
                depMins = convertTotalMinutes(station[3])
            if toStation==station[0]:
                # print("arrtime",arrTIME,station[1])
                arrMins = convertTotalMinutes(station[1])
                # print("delay",delay,station[4])
                deLMins = int(station[4])
        # print(depMins,arrMins,deLMins)
        # pppd= depTimeMins-depMins
        # pppa= arrTimeMins
        dep = (depTimeMins-depMins)**2
        arr = (arrTimeMins-arrMins)**2
        deL = (delay-deLMins)**2
        dist = (dep + arr + deL)**(1/2) 
        # print(dep,arr,deL,"=",dist)
        distList.append([dist,n])
        theList.append([station[2],n])
        n=n+1


    low3list = lowest3(distList)
    #theList = [[actualArrivalTime,index]]
    #distList = [[distance,index]]

    # print("distList",distList)
    # print("theList",theList)
    # print("low3list",low3list)

    # print(trains)

    total=0
    for a in low3list:
        x = theList[a][0]
        # print("AAAA",x)
        x = convertTotalMinutes(x)
        total = total + x #Accumulated total minutes
    total = int(total/len(low3list)) #Average total minutes
    total = TotalMinutesToTime(total) #Time value


    

    # x = str(datetime.timedelta(minutes=total))[:-3] # Convert minutes to time

    arrivalTime = total.replace(":","")

    print("Estimated arrival time at",toStation,"is:", total)

    return total
    

if __name__ == '__main__':
   main("1200","1500","NRW","LST","20")
