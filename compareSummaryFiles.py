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

g_keyword = "blah"

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
    g_keyword = handleNode(prop.getElementsByTagName("keyword1")[0])


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def handleNode(key):
    return getText(key.childNodes)


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

#**********************
# main part here
print '\nCompare two days files to see if there is a difference\n'

previousDay = str(datetime.date.today()-datetime.timedelta(1))
today = str(datetime.date.today())

readPropertyFile()


if compareTwoFiles(previousDay, today, g_keyword) == False:
   print 'Not the same!!!!!'
else:
    print 'the same, no changes'


print '****'
