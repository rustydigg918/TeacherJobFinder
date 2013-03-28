# -*- coding: utf-8 -*-
import shutil
import os
import time
import datetime
import math
import urllib
from array import array
from urlparse import urlparse
from xml.dom import minidom

xml_file = "blah"
g_keyword = "blah"
g_foundOne = False

g_TotalSchools = 0
g_CantSearchSchools = 0

def readTeacherXml():
    readPropertyFile()

    try:

        dom = minidom.parse(xml_file)
        schooldistrict=dom.getElementsByTagName('schooldistrict')
        handleSchooldistricts(schooldistrict)

               
    except Exception, inst:
        print "Unexpected error opening %s: %s" % (xml_file, inst)



def readPropertyFile():
    
    xml_file_property = 'properties.xml'
    try:

        dom = minidom.parse(xml_file_property)
        properties=dom.getElementsByTagName('properties')
        handleProperties(properties)

               
    except Exception, inst:
        print "Unexpected error opening %s: %s" % (xml_file_property, inst)


def handleProperties(properties):
        for prop in properties:
                handleProperty(prop)

def handleProperty(prop):
    global g_keyword
    global xml_file
    g_keyword = handleNode(prop.getElementsByTagName("keyword1")[0])
    xml_file = handleNode(prop.getElementsByTagName("schools")[0])

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def handleSchooldistricts(sds):
        for sd in sds:
                handleSD(sd)

#can decide to search from here.
def handleSD(sd):
    name = handleNode(sd.getElementsByTagName("name")[0])
    url = handleNode(sd.getElementsByTagName("url")[0])

    county = handleNode(sd.getElementsByTagName("county")[0])

# this let's you to search only one county
# would be better not to hardcode the county name
    if county.find('County Name') == -1:
        print 'do morris for now'
        return

    global g_TotalSchools
    global g_CantSearchSchools

    g_TotalSchools = g_TotalSchools + 1
    searchable = handleNode(sd.getElementsByTagName("searchable")[0])
    if searchable.find('False') != -1:
        print 'School: ' + name + ' is not searchable'
        g_CantSearchSchools = g_CantSearchSchools + 1
    else:
        print name + ' ' + url
        searchJob(url, name, county)
    
def handleNode(key):
    return getText(key.childNodes)

def isKeywordFound(fileContents, keyword, lineNumber):
        fileencoding = 'iso-8859-1'
        lowerContents = fileContents.decode(fileencoding)
        lowerContents = lowerContents.lower()
        location = lowerContents.find(keyword)

        if location != -1:
                return True
        return False
        
def schoolName(url):
        o = urlparse(url)
        secondSlash= o.path.find('/', 1)
        returnString = o.netloc + o.path.replace('/', '_')
        if secondSlash != -1:
                        returnString = o.netloc + '_' + o.path[1:secondSlash]        

        return returnString

def copyHTML(fileContents, school):
# create a folder where to copy the html files
        try:
        	os.makededirs(today)
        except OSError as exc:	
                spass

	newSchoolFile = open(today + '/' + school + '.html' ,'w')
	newSchoolFile.write(fileContents)
	newSchoolFile.close()
        
def cantSearch(county, name, url):
    now = datetime.datetime.now()
    today = str(datetime.date.today())

    try:
            os.makedirs('summary')
    except OSError as exc:	
            pass

    cantSearchJobOpenings = open('summary/CantSearchJobs-' + today + '.txt', 'a')
    cantSearchJobOpenings.write(county + ' ' + name + ' ' + url + '.\n')
    cantSearchJobOpenings.close()


################################################################################################
def searchJob(urlToSearch, schoolN, countyName):
    now = datetime.datetime.now()
    today = str(datetime.date.today())

    try:
            os.makedirs('summary')
    except OSError as exc:	
            pass


    print 'url: ' + urlToSearch + ' school: ' + schoolN + ' contry: ' + countyName

    possibleJobOpenings = open('summary/PossibleJobs-' + today + '_' + g_keyword + '.txt', 'a')
    
    # file has the list of job opportunity links for various schools
    #ignore lines which include not applicable because I couldn't find the job openings page

    try:
        urlFilehandle = urllib.urlopen(urlToSearch)
    except :
        print 'got an exception - probably a socket timeout when trying to open: ' + urlToSearch
        return
    

        
    school = schoolName(urlToSearch)

    try:
        global g_foundOne

        print 'Checking ' + school + ' to see if there are any job openings.'
        

        lineNum = 0
        for line in urlFilehandle:
            lineNum = lineNum + 1
            if isKeywordFound(line, g_keyword, lineNum) == True:
                g_foundOne = True
                possibleJobOpenings.write(countyName + ' - ' + schoolN + ' maybe see ' + urlToSearch + '\n')
                possibleJobOpenings.close()
                return

        possibleJobOpenings.close()
        
    except OSError as exc:
        print 'error*****'
        pass

###### tell me what in fileTwoDate that isn't in fileOneDate
def summarizePreviousTwoDays(fileOneDate, fileTwoDate, keyword):
    
    summaryFileOne = open('summary/PossibleJobs-' + fileOneDate + '_' + keyword + '.txt', 'r')
    summaryFileTwo = open('summary/PossibleJobs-' + fileTwoDate + '_' + keyword + '.txt', 'r')

    fileOne = summaryFileOne.readlines()
    fileTwo = summaryFileTwo.readlines()

    summaryFileOne.close()
    summaryFileTwo.close()

    outFile = open("summary/Diff.txt", 'a')
    lineNum = 0


    flag = False
    
    for lineF2 in fileTwo:
        for lineF1 in fileOne:
            if lineF1 == lineF2:
                flag = True
                pass
                                        
        if flag == False:
            print "**** Differences, see summary/Diff.txt ****"
            outFile.write(fileTwoDate + " check " + lineF2)
        flag = False

    
    
    outFile.close()
    return



def compareTwoFiles(fileOneDate, fileTwoDate, keyword):
    summaryFileOne = open('summary/PossibleJobs-' + fileOneDate + '_' + keyword + '.txt', 'r')
    summaryFileTwo = open('summary/PossibleJobs-' + fileTwoDate + '_' + keyword + '.txt', 'r')

    fileOne = summaryFileOne.readlines()
    fileTwo = summaryFileTwo.readlines()

    summaryFileOne.close()
    summaryFileTwo.close()

    outFile = open("summary/results.txt", 'a')
    lineNum = 0

    if len(fileOne) != len(fileTwo):
        print "File: " + str(fileOneDate) + " len: " + str(len(fileOne)) + " is different from " + str(fileTwoDate) + " array size " + str(len(fileTwo)) + ".\n"
        
        outFile.write("File: " + str(fileOneDate) + " is different from " + str(fileTwoDate) + " array size different.\n")


        if len(fileOne) < len(fileTwo):
                for lineF1 in fileOne:
                    if lineF1 != fileTwo[lineNum]:
                        outFile.write('File: ' + str(fileOneDate) + ' is different from ' + str(fileTwoDate) + '\nfile 1: ' + lineF1 + '.\n vs\nfile 2: ' + fileTwo[lineNum] + '.\n')
                        outFile.close()
                        return False
                        
                    lineNum += 1

        outFile.close()
        return False

    lineNum = 0
    
    isSame = True
    for lineF1 in fileOne:
        if lineF1 != fileTwo[lineNum]:
            outFile.write('File: ' + str(fileOneDate) + ' is different from ' + str(fileTwoDate) + '\nfile 1: ' + lineF1 + '.\n vs\nfile 2: ' + fileTwo[lineNum] + '.\n')
            isSame = False
        lineNum += 1

    if isSame == True:
            outFile.write('File: ' + str(fileOneDate) + ' is the same as ' + str(fileTwoDate) + '.\n')
        
    outFile.close()
    return isSame

#*****************************Main method
# main part here

today = str(datetime.date.today())
previousDay = str(datetime.date.today()-datetime.timedelta(1))
today = str(datetime.date.today())

readPropertyFile()

# set to 1 == 2 to skip this block of code
if 1 == 1:
	
    readTeacherXml()

    print '****'
    if g_foundOne == True:
        print 'Done. Check summary/PossibleJobs-' + today + '.txt'
    else:
        print 'Done. No leads.'

    g_TotalSchools
    g_CantSearchSchools
    failP = 0
    if g_TotalSchools != 0:
        failP = (1.0 * g_CantSearchSchools / g_TotalSchools) * 100
        
    print '\nSearched ' + str(g_TotalSchools) + ' and ' + str(g_CantSearchSchools) + ' failed to search, for a fail % of ' + str(failP) + '.\n' 

    print '\nCompare two days files to see if there is a difference\n'



# skip this block of code
# this block is a quick test of the compare function without searching websites for the current day
    if 1 == 2:
        ########
        #
        if compareTwoFiles(previousDay, today, g_keyword) == False:
            print 'Not the same!!!!!'
        else:
            print 'the same, no changes'

    print '****'



    try:

        summarizePreviousTwoDays(previousDay, today, g_keyword)
    
    except Exception, inst:
        print "Unexpected error comparing today and the previous day: %s" % (inst)
