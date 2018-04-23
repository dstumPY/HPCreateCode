"""
Dieses Skript berechnet aus den Eingaben des Nutzers die Daten für sich wiederholende Events (bspw. wöchentlich) und gibt
die Eventsammlung als HTML-Code aus. 
Es gibt zwei verschiede Eventtypen, welche als eigene Klassen angelegt werden: wiederkehrende Events 
(continuousTimeObject) und einzeln auftretende Events (singleTimeObject). Diese beiden Klassen erben von der Superklasse timeObject.

Klasse timeObject:
	Attribute:
		timeUNIX : 		speichert aktuellen Unix-Timestamp (Int)
		timeSTRUCT: 	speichert Unix-Timestamp im struct-Format (Struct)
		RepeatInSec:	Wiederholdauer in Sekunden (Int)
		PlannedDates:	Liste mit den berechneten Daten der Events (List)
		BeginHour:		Zeitpunkt des Beginns in Stunden (Int)
		BeginMin:		Zeitpunkt des Beginns in Minuten (Int)
	
	Klassenmethoden:
		addSec: 		Addiert Sekunden auf timeUNIX (inkl. timeSTRUCT)
		incrToTime:		Setzt timeUNIX bzw. timeSTRUCT vom aktuellen zeitpunkt auf den ersten berechneten Zeitpunkt
		
Klasse continuousTimeObject (erbt von timeObject)
	Attribute:
		dayOfWeek:		Speichert den Wochentag für wöchentlich wiederkehrende Events
		
	Klassenmethoden:
		incrToDayOfWeek:Setzt timeUNIX bzw. timeSTRUCT auf das nächste Datum, das zum Wochentag (dayOfWeek) passt
		createDataTable:Berechnet wiederholende Daten des aktuellen Monats und speichert diese in PlannedDates
		setTimeObject:	Setzt timeUNIX (inkl. timeSTRUCT) auf bestimmten Timestamp und erhöht, bis dayOfWeek erreicht ist

Klasse singleTimeObject erbt von timeObject
	Bemerkung: 	Da sich die Struktur zu wiederholenden Events unterscheidet (hier sind Daten im Struct-Format notwendig),
				muss eine separate Klasse erstellt werden, in welcher der Konstruktor entsprechend angepasst werden kann
	
	Attribute:	keine weiteren
	
	Methoden:	
		createDataTable:Analog zu oben, einelementige Liste
"""

import time
import re
from pip._vendor.progress import counter

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
        self.timeSTRUCT = time.struct_time((int(year),int(month),int(day),int(beginHOUR),int(beginMINUTE),0,0,0,0))
        self.timeUNIX = time.mktime(self.timeSTRUCT)
        self.BeginHour = beginHOUR
        self.BeginMin = beginMINUTE
        self.EndHour = endHOUR
        self.EndMin = endMINUTE
    
    def createDataTable(self):
        self.PlannedDates.append(self.timeUNIX)
        print(self.timeSTRUCT)

# nimmt Dictionary bestehend aus Unix-Timestamp-timeObject-Zuordnung und generiert hieraus HTML-Code        
def writeOutput(dic):
	currentDate = time.time()
	currentDate = time.gmtime(currentDate)
	print(currentDate)
	translateDays = {"Monday" : "Montag", "Tuesday" : "Dienstag" , "Wednesday" : "Mittwoch" , "Thursday" : "Donnerstag" , "Friday" : "Freitag" , "Saturday" : "Samstag" , "Sunday" : "Sonntag"}
	translateMonths = {"January" : "Januar", "February" : "Februar", "March" : "März", "April" : "April", "May" : "Mai", "June" : "Juni", "July" : "Juli", "August" : "August", "September" : "September", "October" : "Oktober", "November" : "November" , "December" : "Dezember"}
	timeFormat = {"0" : "00" , "1" : "01", "2" : "02", "3" : "03" ,"4" : "04", "5" : "05", "6" : "06", "7" : "07", "8" : "08", "9" : "09","10" : "10", "11" : "11", "12" : "12", "13" : "13", "14" : "14", "15" : "15", "16" : "16", "17" : "17", "18" : "18", "19" : "19", "20" : "20", "21" : "21", "22" : "22", "23" : "23", "24" : "24", "25" : "25", "26" : "26", "27" : "27", "28" : "28", "29" : "29", "30" : "30", "31" : "31", "32" : "32", "33" : "33", "34" : "34", "35" : "35", "36" : "36", "37" : "37", "38" : "38", "39" : "39", "40" : "40", "41" : "41", "42" : "42", "43" : "43", "44" : "44", "45" : "45", "46" : "46", "47" : "47", "48" : "48", "49" : "49", "50" : "50", "51" : "51", "52" : "52", "53" : "53", "54" : "54", "55" : "55", "56" : "56", "57" : "57", "58" : "58", "59" : "59"}
	tmpString = "HP_EVENTCODE_" + str(currentDate.tm_mday) + "-" + str(currentDate.tm_mon) + "-" + str(currentDate.tm_year) + ".txt"
	fobj = open(tmpString, "w")
	#fobj.write("Hallo")
	for dicElement in sorted(dic.keys()):
		tmpVar1 = time.strftime("%A" , time.gmtime(int(dicElement))) 
		tmpVar2 = time.strftime("%B", time.gmtime(int(dicElement)))
		tmpVar3 = time.strftime("%d", time.gmtime(int(dicElement)))
		bufferString = '<div class="title-wrapper"><strong>' + translateDays[tmpVar1] + ", " + tmpVar3 + ". " + translateMonths[tmpVar2] + "</strong></div>\n"
		bufferString = bufferString + '<div class="title-wrapper">' + timeFormat[str(dic[dicElement].BeginHour)] + ":" + timeFormat[str(dic[dicElement].BeginMin)] + "-" + timeFormat[str(dic[dicElement].EndHour)] + ":" + timeFormat[str(dic[dicElement].EndMin)] + '<span class="event-title" style="color: #a32929;">&nbsp;</span></div>' + "\n"
		bufferString = bufferString + '<div class="title-wrapper"><span class="event-title" style="color: #a32929;">&nbsp;' + str(dic[dicElement].EventName) + "</span></div>\n"
		bufferString = bufferString + '<div class="title-wrapper"></div>\n'
		fobj.write(bufferString)	
	fobj.close()
		
#löscht Eintrag aus Dictionary	
def deleteDictEntry(dic):
    delDictEntry = input('Welches Datum soll geloescht werden (Unix timestamp)? :')
    del dic[int(delDictEntry)]

# Einlesen der Daten für wiederkehrende Events
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
	    x.setTimeObject(x.timeUNIX)	#setzt UNIXtimestamp
	    x.createDataTable()
	    userInformation.append(x)
	    answer = input('Soll ein weiteres wiederkehrendes Event angelegt werden?:')

# Methode zum Einlesen für einzelne Events
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

# Methode zum Löschen von Events aus PlannedDates
def deleteEventFromList():
	global userInformation
	global counter
	answer = input('Soll ein Event gelöscht werden? (y/n):')
	while answer != 'n':
		delEvent = int(input('Zu welchem Timestamp soll ein Event gelöscht werden?:'))
		for x in userInformation:
			for y in x.PlannedDates:
				if int(y) == int(delEvent):
					x.PlannedDates.remove(y)
		answer = input('Soll ein Event gelöscht werden? (y/n):')





# MAIN

global userInformation
userInformation = []
global answer
answer = 'y'
global counter
counter = 1
createContinuousEvents()
createSingleEvents()
for x in userInformation:			# alle bisher erzeugten Elemente werden ausgegeben, um Löschen zu ermöglichen
	for y in x.PlannedDates:
		print(y)
		print(time.gmtime(y))
		#print(y.timeSTRUCT)		
deleteEventFromList()

UNIXTimeTable = {}
#tmp_iter1 = 0
for x in userInformation:
	print(x.timeSTRUCT)
	print('###')
	#tmp_iter2 = 0
	for y in x.PlannedDates:
		UNIXTimeTable[y] = x				#legt Dictionary mit UNIXTimestamps als keys: UNIXTimeTable = {151715880 : 0x01fA...}

writeOutput(UNIXTimeTable)


###############
#	TESTS	  #
###############

#Test zum Löschen von Dictionary-Entries
"""
print(UNIXTimeTable)   
deleteDictEntry(UNIXTimeTable)
print(UNIXTimeTable)
"""

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

#Speziellen UNIXTimeStemp für erzeugtes timeObject setzen
"""
K1.setTimeObject(time.time()-24*86400)
print(K1.timeUNIX)
print(K1.timeSTRUCT)
"""

#Create Test Data 
"""
userInformation = []
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
		UNIXTimeTable[y] = x				#legt Dictionary mit UNIXTimestamps als keys: UNIXTimeTable = {151715880 : 0x01fA...}
	
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


