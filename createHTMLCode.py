import time
import re

class timeObject():
	def __init__(self,repeatInSec,begin,end,eventName):
		x = time.time()
		self.timeUNIX = x
		self.timeSTRUCT = time.gmtime(x)
		self.RepeatInSec = repeatInSec
		self.PlannedDates = []
		res_begin = re.search("(\d\d|\d)\:(\d\d|\d)",begin)
		while not res_begin or (int(res_begin.group(1)) > 23) or (int(res_begin.group(2)) > 59):
			begin = input('Startzeit bitte im Format HH:MM eingeben: ')
			res_begin = re.search("(\d\d|\d)\:(\d\d|\d)",begin)            
		if res_begin:
			self.BeginHour = int(res_begin.group(1))
			self.BeginMin = int(res_begin.group(2))
		res_end = re.search("(\d\d|\d)\:(\d\d|\d)",end)
		while not res_end or (int(res_end.group(1)) > 23) or (int(res_end.group(2)) > 59):
			begin = input('Endzeit bitte im Format HH:MM eingeben: ')
			res_end = re.search("(\d\d|\d)\:(\d\d|\d)",end)    
		if res_end:
			self.EndHour = int(res_end.group(1))           
			self.EndMin = int(res_end.group(2))           
		self.EventName = eventName
	
	def addSec(self,seconds):
		self.timeUNIX += seconds
		self.timeSTRUCT = time.gmtime(self.timeUNIX)    
        
	def incrToTime(self):
		print(self.BeginHour)
		print(self.BeginMin)
		print(self.EndHour)
		print(self.EndMin) 
		self.timeSTRUCT = time.struct_time((self.timeSTRUCT.tm_year,self.timeSTRUCT.tm_mon,self.timeSTRUCT.tm_mday,self.BeginHour,self.BeginMin,0,self.timeSTRUCT.tm_wday,self.timeSTRUCT.tm_yday,self.timeSTRUCT.tm_isdst))
		self.timeUNIX = time.mktime(self.timeSTRUCT)
		
class continuousTimeObject(timeObject):	
	def __init__(self,dayOfWeek,repeatInSec,begin,end,eventName):
		timeObject.__init__(self,repeatInSec,begin,end,eventName)
		self.DayOfWeek = dayOfWeek
		self.incrToDayOfWeek()	# Methodenaufruf bewirkt Setzen des gesuchten Anfangsdatums für das erzeugt Objekt

	def incrToDayOfWeek(self):
		while self.timeSTRUCT.tm_wday != self.DayOfWeek:
			self.addSec(86400)

	def createDataTable(self):
		self.incrToTime()
		self.incrToDayOfWeek()
		actualMonth = self.timeSTRUCT.tm_mon
		#self.PlannedDates.append(self.timeUNIX)
		while self.timeSTRUCT.tm_mon == actualMonth:
			self.PlannedDates.append(self.timeUNIX)
			print(self.timeSTRUCT)
			self.addSec(self.RepeatInSec)
			
	#Setzt erzeugte Objekte auf speziellen UNIXTimeStemp (wichtig für Tests)
	
	def setTimeObject(self,UNIXTimeStemp):
		self.timeUNIX = UNIXTimeStemp
		self.timeSTRUCT = time.gmtime(UNIXTimeStemp)
		self.incrToDayOfWeek()
		
class singleTimeObject(timeObject):
    def __init__(self,day,month,year,beginHOUR,beginMINUTE,endHOUR,endMINUTE,eventName):
        timeObject.__init__(self,0,str(str(beginHOUR) + ":" + str(beginMINUTE)),str(str(endHOUR) + ":" + str(endMINUTE)),eventName)
#eigentlich vorher noch day, month,year auf Format prüfen
        self.timeSTRUCT = time.struct_time((int(year),int(month),int(day),int(beginHOUR),int(beginMINUTE),0,0,0,0))
        self.timeUNIX = time.mktime(self.timeSTRUCT)
        self. BeginHour = beginHOUR
        self.BeginMin = beginMINUTE
        self.EndHour = endHOUR
        self.EndMin = endMINUTE
    
    def createDataTable(self):
        self.PlannedDates.append(self.timeUNIX)
        print(self.timeSTRUCT)
        
def writeOutput(dic):
	currentDate = time.time()
	currentDate = time.gmtime(currentDate)
	print(currentDate)
	translateDays = {"Monday" : "Montag", "Tuesday" : "Dienstag" , "Wednesday" : "Mittwoch" , "Thursday" : "Donnerstag" , "Friday" : "Freitag" , "Saturday" : "Samstag" , "Sunday" : "Sonntag"}
	tmpString = "Schovelkoten_HP_EVENTCODE_" + str(currentDate.tm_mday) + "-" + str(currentDate.tm_mon) + "-" + str(currentDate.tm_year) + ".txt"
	fobj = open(tmpString, "w")
	#fobj.write("Hallo")
	for dicElement in sorted(dic.keys()):
		tmpVar = time.strftime("%A" , time.gmtime(int(dicElement))) 
		bufferString = '<div class="title-wrapper"><strong>' + translateDays[tmpVar] + "\n"
		fobj.write(bufferString)	
	fobj.close()
		
		
def deleteDictEntry(dic):
    delDictEntry = input('Welches Datum soll geloescht werden (Unix timestamp)? :')
    del dic[int(delDictEntry)]

#wahrscheinlich unnötig    
def insertSinglEvent(dic):
    date = input('Zu welchem Datum soll ein Event angelegt werden? (DD:MM:YYYY)')
    res_date = re.search("(\d\d)[\.\:\,\;\-](\d\d)[\.\:\,\;\-](\d\d\d\d)",date)
    while not res_date.group(1) or res_date.group(2) or res_date.group(3):
        date = input('Die Eingabe war fehlerhaft. Event bitte erneut eigeben? (DD:MM:YYYY)')
        res_date = re.search("(\d\d)[\.\:\,\;\-\/](\d\d)[\.\:\,\;\-\/](\d\d\d\d)",date)
    time_begin = input('Wann startet das Event? (HH:MM)')
    res_begin = re.search("(\d\d)[\.\:\,\;\-\/](\d\d)",time_begin)
    while not (res_begin.group(1) or res_begin.group(2)):
        time_begin = input('Die Eingabe war fehlerhaft. Startzeit bitte erneut eigeben? (DD:MM:YYYY)')
        res_begin = re.search("(\d\d)[\.\:\,\;\-\/](\d\d)",time_begin)
    time_end = input('Wann endet das Event? (HH:MM)')
    res_end = re.search("(\d\d)[\.\:\,\;\-\/](\d\d)",time_end)
    while not (res_end.group(1) or res_end.group(2)):
        time_end = input('Die Eingabe war fehlerhaft. Endzeit bitte erneut eigeben? (DD:MM:YYYY)')
        res_end = re.search("(\d\d)[\.\:\,\;\-\/](\d\d)",time_end)
    if res_date and res_begin and res_end:
        singleTimeElement=singleTimeObject(int(res_date.group(1)),int(res_date.group(2)),int(res_date.group(3)),int(res_begin.group(1)),int(res_begin.group(2)),0,0,0,0)
    else:
        print('Match hat nicht funktioniert.')
#hier muss noch der Rest gefüllt werden

def createContinuousEvents():
    global userInformation
    global answer
    global counter
    while answer != 'n':
	    i = input('Event ' + str(counter) + ' - Wochentag (0-6):')
	    print()
	    j = input('Event ' + str(counter) + ' - Wiederholung (Woche = 604800):')
	    print()
	    k = input('Event ' + str(counter) + ' - Beginn: (HH:MM)')
	    print()
	    l = input('Event ' + str(counter) + ' - Ende: (HH:MM)')
	    print()
	    m = input('Event ' + str(counter) + ' - Eventname:')
	    counter = counter + 1
	    x = continuousTimeObject(int(i),int(j),k,l,m)
	    x.setTimeObject(x.timeUNIX-16*86400)	#setzt UNIXtimestamp um 16 Tage zurück
	    x.createDataTable()
	    userInformation.append(x)
	    answer = input('Soll ein weiteres wiederkehrendes Event angelegt werden?:')

def createSingleEvents():
    global userInformation
    global answer
    global counter
    answer = input('Soll ein SingleEvent angelegt werden?:')
    while answer != 'n':
        TMPSingleYear = input('Event ' + str(counter) + ' - Jahr: (YYYY)')
        print()
        TMPSingleMonth = input('Event ' + str(counter) + ' - Monat: (MM/M)')
        print()
        TMPSingleDay = input('Event ' + str(counter) + ' - Tag (DD/D):')
        print()
        TMPSingleBegin = input('Event ' + str(counter) + ' - Beginn: (HH:MM)')
        print()
        res_singleBegin = re.search("(\d\d|\d)\:(\d\d|\d)", TMPSingleBegin)
        while not res_singleBegin or (int(res_singleBegin.group(1)) > 23 ) or (int(res_singleBegin.group(2)) > 59):
            TMPSingleBegin = input('Bitte korrektes Format (HH:MM) eingeben:')
            res_singleBegin = re.search("(\d\d|\d)\:(\d\d|\d)", TMPSingleBegin)
        TMPSingleBeginHOUR = int(res_singleBegin.group(1))
        TMPSingleBeginMIN = int(res_singleBegin.group(2))
        TMPSingleEnd = input('Event ' + str(counter) + ' - Ende: (HH:MM)')
        print()
        res_singleEnd = re.search("(\d\d|\d)\:(\d\d|\d)", TMPSingleEnd)
        while not res_singleEnd or (int(res_singleEnd.group(1)) > 23 ) or (int(res_singleEnd.group(2)) > 59):
            TMPSingleEnd = input('Bitte korrektes Format (HH:MM) eingeben:')
            res_singleEnd = re.search("(\d\d|\d)\:(\d\d|\d)", TMPSingleEnd)
        TMPSingleEndHOUR = int(res_singleEnd.group(1))
        TMPSingleEndMIN = int(res_singleEnd.group(2))
        TMPSingleEvent = input('Event ' + str(counter) + ' - Eventname:')
        x=singleTimeObject(TMPSingleDay,TMPSingleMonth,TMPSingleYear,TMPSingleBeginHOUR,TMPSingleBeginMIN,TMPSingleEndHOUR,TMPSingleEndMIN,TMPSingleEvent)
        x.createDataTable()
        userInformation.append(x)
        answer = input('Soll ein weiteres SingleTime Event angelegt werden?:')

def getEventInformation():
    global userInformation
    userInformation = []
    global answer
    answer = 'y'
    global counter
    counter = 1
    createContinuousEvents()
    createSingleEvents()
    for x in userInformation:
        for y in x.PlannedDates:
            print(y)
            print(time.gmtime(y))
            #print(y.timeSTRUCT)
    


#Speziellen UNIXTimeStemp für erzeugtes timeObject setzen
"""
K1.setTimeObject(time.time()-24*86400)
print(K1.timeUNIX)
print(K1.timeSTRUCT)
"""

#Create Test Data 
"""
x=continuousTimeObject(6,604800,'16:00','18:00','HSP')
x.setTimeObject(x.timeUNIX-16*86400)
x.createDataTable()
userInformation.append(x)
y=continuousTimeObject(2,604800,'18:00','20:00','BSG')
y.setTimeObject(y.timeUNIX-16*86400)
y.createDataTable()
userInformation.append(y)
z=singleTimeObject(22,2,2018,17,18,19,20,'FunnyTest')
z.createDataTable()
userInformation.append(z)

UNIXTimeTable = {}
#tmp_iter1 = 0
for x in userInformation:
	print(x.timeSTRUCT)
	print('###')
	#tmp_iter2 = 0
	for y in x.PlannedDates:
		UNIXTimeTable[y] = x				#Dictionary mit UNIXTimestamps als keys
	
for i in sorted(UNIXTimeTable.keys()):
	#print(UNIXTimeTable[i].timeUNIX)
    print(int(i))
    print(time.gmtime(int(i)))
    print(UNIXTimeTable[i].BeginHour)
    print(UNIXTimeTable[i].BeginMin)
    print(UNIXTimeTable[i].EndHour)
    print(UNIXTimeTable[i].EndMin)
    print(UNIXTimeTable[i].EventName)
"""

# MAIN

getEventInformation()

"""
while answer != 'n':
	i = input('Event ' + str(counter) + ' - Wochentag (0-6):')
	print()
	j = input('Event ' + str(counter) + ' - Wiederholung (Woche = 604800):')
	print()
	k = input('Event ' + str(counter) + ' - Eventname:')
	print()
	l = input('Event ' + str(counter) + ' - Beginn:')
	print()
	m = input('Event ' + str(counter) + ' - Ende:')
	counter = counter + 1
	x = timeObject(int(i),int(j),k,l,m)
	x.setTimeObject(x.timeUNIX-24*86400)	#setzt UNIXtimestamp um 24 Tage zurück
	x.createDataTable()
	userInformation.append(x)
	answer = input('Soll ein weiteres Event angelegt werden?:')
"""



#Test zum Löschen von Dictionary-Entries


#print(UNIXTimeTable)   
#deleteDictEntry(UNIXTimeTable)
#print(UNIXTimeTable)

#writeOutput(UNIXTimeTable)

#print('#################')		
#for x in UNIXTimeTable:
#	print(time.gmtime(x))

#print('#################')		
#for x in UNIXTimeTable:
#	print(time.gmtime(x))


#Test der erzeugten Liste PlannedDates

"""
print('####')
for x in K1.PlannedDates:
    print(time.gmtime(x))
"""

#Test der Klassenfunktion addSec

"""
K1.addSec()
"""


