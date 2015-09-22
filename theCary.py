######################################################################################
##                                                                                  ##
## Program: theCary.py                                                              ##
## Purpose: To retrive from "The Cary" events web page a list of all events.        ##
## Author:  Robert Campbell - rcampbellnc@gmail.com                                 ##
## Created: 04 Nov 2014                                                             ##
## Updated: 05 Nov 2014                                                             ##
##                                                                                  ##
## Change Log:                                                                      ##
## 04 Nov 2014 - Initial creation                                                   ##
## 05 Nov 2014 - Basic operation successful, added comments to code                 ##
##                                                                                  ##
######################################################################################

#needed for http requests
import requests
#needed to effeciently hack through the HTML
import bs4
#needed so we can use a little bit of regex
import re
#we need to parse some JSON for movie info, so we need
import json

#I want to know how many events there are
eventCount = 0

#fetch the events page from the website
response = requests.get('http://www.thecarytheater.com/events/')

#toss that into soup
soup = bs4.BeautifulSoup(response.text)

#print soup

#for every div that has post-xxx in it (using regex, via re module)
for node in soup.findAll('div', { "class" : re.compile('^post-')}):
	#pass the node through BeautifulSoup into workNode, we'll use that below
	workNode = bs4.BeautifulSoup(node.text)
	#grab the div that containes the Title information
	detailTitle = node.select('div.event-left')
	#now, we need to massage this due to some non-ascii characters in this text!
	#grab the string into modifiedTitle
	modifiedTitle = str(detailTitle)
	#now, using regexp, courtesy of the re module, change any non-Ascii sequence to nothing ('')
	modifiedTitle = re.sub(r'[^\x00-\x7F]+','', modifiedTitle)
	#Now, we'll use the non-ascii-vanquished title and put that into BeautifulSoup, we need to go find the Title
	workTitle = bs4.BeautifulSoup(str(modifiedTitle))
	#the title in a part of the <a href... tag, let's grab that
	titleAnchor = workTitle.find('a')
	#and let's get the title part into our titleName variable, FINALLY we have a good title with all ascii characters!!!
	titleName = titleAnchor['title']

	#grap the Date info
	infoDate = node.select('div.event-date')
	#parse out of the div the individual elements we want, the date info in this case
	#stuff the div back into a BeautifulSoup object
	workDate = bs4.BeautifulSoup(str(infoDate))
	#grab the Month part
	infoMonth = workDate.find('span', { "class" : 'month'})
	#grab the day (number) part
	infoDay = workDate.find('span', { "class" : 'day'})
	#grab the weekday (name) part
	infoWeekday = workDate.find('span', { "class" : 'weekday'})

	#Begin work on next DIV chunk here
	#grab the Details info, this has title, time, cost and rating
	infoDetails = node.select('div.event-details')
	#Pass the info Details div info through Beautifulsoup
	workDetails = bs4.BeautifulSoup(str(infoDetails))
	#get the event heading div - this has heading info for the event
	detailHeading = workDetails.find('span', { "class" : 'event-heading'})
	#because there is a tendency to use non-ascii, let's get the string of our stripped text
	modifiedHeading = detailHeading.text.strip()
	#now reset our detailHeading to be a string with all non-ascii replaced thanks to regexp
	detailHeading = re.sub(r'[^\x00-\x7F]+','', modifiedHeading)
	#grab the Time info
	detailTime = workDetails.find('span', { "class" : 'event-time'})
	#grab the Price info
	detailPrice = workDetails.find('span', { "class" : 'ticket-price'})
	#grab the venue notes - usually this where the movie rating is listed
	detailNotes = workDetails.find('span', { "class" : 'venue-notes'})

	eventCount += 1

	#print out a dump of the info we've worked so hard to collect!
	print infoWeekday.text + ', ' + infoMonth.text + ' ' +infoDay.text + ' ' + detailTime.text.strip() + ' ' + detailHeading + ' ' + titleName + ' ' + detailTime.text.strip() + ' ' + detailPrice.text.strip() + ' ' + detailNotes.text.strip()   
	#and add a line in the stdout as a demarc
	#print "**********************************************************************" 

    #end of for loop

#How many events?
print "Total: " + str(eventCount)

#end program