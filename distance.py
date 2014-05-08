import os, urllib, urllib2, time, csv 
from xml.dom.minidom import parseString
#url = "http://maps.googleapis.com/maps/api/directions/xml?origin=" + "40.63319,-73.99440" + "&destination=" + "42.25446,-92.21648" + "&sensor=false"
#url = "http://maps.googleapis.com/maps/api/distancematrix/xml?origins=" + "40.63319,-73.99440" + "&destination=" + "42.25446,-92.21648" + "&sensor=false"
#url = "http://maps.googleapis.com/maps/api/distancematrix/xml?origins=40.63319,-73.99440&destinations=San+Francisco|Victoria+BC&sensor=false"



def getDistance(origin, destinations):
	url = "http://maps.googleapis.com/maps/api/distancematrix/xml?origins="
	url = url + origin + "&destinations="
	for dest in destinations:
		url = url + dest + "|"
	url = url[0:len(url)-1]
	url = url + "&sensor=false"
	print url
	#parsing the xml reply from google map
	xmlFile = urllib.urlretrieve(url,'test.xml')
	xmlFileOpen = urllib2.urlopen(url).read()
	xmlFileDom = parseString(xmlFileOpen)
	distances = []
	for i in range(len(destinations)):
		distances.append(xmlFileDom.getElementsByTagName("DistanceMatrixResponse")[0].getElementsByTagName("row")[0].getElementsByTagName("element")[i].getElementsByTagName("distance")[0].getElementsByTagName("text")[0].toxml().replace('<text>','').replace('</text>',''))
	return distances

#print getDistance("40.63319,-73.99440",["Victoria+BC","42.25446,-92.21648"])
