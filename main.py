#!/usr/bin/env python
# encoding=utf8 
# -*- coding: utf-8 -*-

# Created by André Wisén
# Based on API and resources of Hittapunktse AB
# 
# For more info, read the README at my GitHub
# http://github.com/andrewisen/AI2102-D4

import sys
import time
import random
import string
import hashlib
import httplib
import json
import csv
import math 

#################
#### CLASSES ####
#################

# === SETTINGS ===
# 

class createSettings:
    def __init__(self):
        self.geoDist = 2000
        self.tradeMaxCount = 4


# ==== AUTHENTICATION ===
#
# Creates a unique user for authentication
# READ MORE: http://hitta.github.io/public/http-api/authentication.html

class createUser:
    def __init__(self):
        # Get your Caller ID and Private API Key at https://www.hitta.se/api (in Swedish)

        self.callerID = " CALLER ID "
        self.key =  " API KEY "

# ==== PROJECTS ===
#
# Creates a OBJECT for each "project"
# The coordinate system is Swedish grid (RT90).
# It's an old Swedish standard, but it's the default used by hitta.se
# You can convert between RT90 and more modern ones.
# 
# Note: Outputs may be in a more modern coordinate system.

class createProjectA:
    def __init__(self):
        self.name = "Dalenum"
        self.x = 6582786 # RT90
        self.y = 1633843 # RT90

class createProjectB:
    def __init__(self):
        self.name = "Norra Djurgårdsstaden"
        self.x = 6583522 # RT90
        self.y = 1632159 # RT90

class createProjectC:
    def __init__(self):
        self.name = "Gåshaga"
        self.x = 6584478 # RT90
        self.y = 1637852 # RT90

# === HEADER ===
#
# Creates a temporary header
# It's temporary because the hashed string is based on Time
# (and can therefore not be re-used in other calls)
#
# NOTE: The script creates a new object each time.
#       A suggestion is to just change the attributes instead

class createHeader: 
    def __init__(self, user):
     
        self.tempTime = str(int(time.time()))
        self.tempRandom = "".join(random.choice(string.letters + string.digits + string.punctuation) for _ in range(16))

        self.tempString = user.callerID + self.tempTime + user.key + self.tempRandom
        self.hashedString = hashlib.sha1(self.tempString).hexdigest()

        # The HTTP Header(s)
        self.headers = {
           "X-Hitta-CallerId": user.callerID,
           "X-Hitta-Time": self.tempTime,
           "X-Hitta-Random": self.tempRandom,
           "X-Hitta-Hash": self.hashedString
        }

# === URL ===
# 
# Creates the base for the url OBJECT.
# This class uses methods to change the attribute

class createURL:
    def __init__(self):
        self.url = "null"

    def get(self):
        return self.url

    def set(self, url):
        self.url = url


#################
#### METHODS ####
#################

def getCompIDs():
    compIDs = {}

    with open("comID.csv", 'rU') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            try:
                if row[0].split(";")[3] == "Yes":
                    key = row[0].split(";")[1]
                    name = row[0].split(";")[0]
                    cat = row[0].split(";")[2]
                    compIDs[key] = [name,cat]
            except:
                continue
    return compIDs

def getData(user, project, compIDs, settings):
    print "Getting data\nPlease wait..."
    response = []

    for eachProject in project:
        for eachComp in compIDs:
            url = getURL(user, eachProject, eachComp, settings)
            eachResponse = getResponse(user, eachProject, url, compIDs, eachComp)
            response.append(eachResponse)

    return response

def getURL(user, eachProject, eachComp, settings):
    # Based on http://hitta.github.io/public/http-api/search/trades.html

    geoPoint = str(eachProject.x) + ":" + str(eachProject.y)
    url = "https://api.hitta.se/publicsearch/v1/companies/trade/" + str(eachComp) + "/nearby/" + str(geoPoint) + "?geo.distance=" + str(settings.geoDist) + "&trade.max.count=" + str(settings.tradeMaxCount) + "&geo.system=RT90"

    return url

def getResponse(user, eachProject, url,compIDs,eachComp):
    eachResponse = []

    # Creates the header for the API Call
    # Each call needs a new header, since the header contains a unique hased key (based on time)
    headers = createHeader(user)

    try:
        # HTTP GET Request
        conn = httplib.HTTPSConnection("api.hitta.se")
        conn.request("GET", url, "", headers.headers)
        resp = conn.getresponse() 

    except:
        print "ERROR: Can't connect to API"
        exit()



    jsonResponse = json.loads(resp.read())
    
    # === DEBUG ===
    # Print JSON Response
    # I.e. Print everything
    # 
    # print json.dumps(jsonResponse, indent=4, separators=(',', ': '))


    while True:
        try:
            # ssadasd
            compDict = jsonResponse["result"]["companies"]["company"]


            for eachValue in compDict:
                companyName = eachValue["displayName"]
                
                north = str(eachValue["address"][0]["coordinate"]["north"])
                east = str(eachValue["address"][0]["coordinate"]["east"])

                dist = str(getDist(eachProject, north, east))

                string = eachProject.name + ";" + companyName + ";" + north + ":" + east + ";" + dist + ";" + compIDs[eachComp][1] + ";" + compIDs[eachComp][0] 
                eachResponse.append(string)

            break

        except KeyError:
            break

        except:
            print "No companies found"
            raise
            quit()
            #continue

    return eachResponse
        
def clearFile():
        f = open("output.csv", "w")
        f.truncate()
        f.close()

def writeSomething(response):
    clearFile()

    with open('output.csv','wb') as file:
        file.write("Project;Company;GeoPoint;Dist;Cat;SubCat")
        file.write('\n')
        for eachResponse in response:
            for eachLine in eachResponse:
                file.write(eachLine.encode("utf-8"))
                file.write('\n')

def getDist(eachProject, north, east):
    x1, x2 = int(eachProject.x), int(north.split(".")[0])
    y1, y2 = int(eachProject.y), int(east.split(".")[0])

    x_prim = pow((x2 - x1),2)
    y_prim = pow((y2 - y1),2)

    # Euclidean distance in meters
    dist = math.sqrt(x_prim + y_prim)
    
    return dist




def main():
    # === FIX UNICODE ===
    #
    # An ugly work around the unicode issue
    # READ MORE: https://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte

    reload(sys)  
    sys.setdefaultencoding('utf8')

    # === AUTHENTICATION === 
    #
    # Each API Call needs authentication
    # To authenticate you need
    #   1) callerId
    #   2) private API key 
    # 
    # READ MORE: http://hitta.github.io/public/http-api/authentication.html (Swedish)

    user = createUser()

    # === DEFINE PROJECTS ===
    #
    # There are three (3) different "projects".
    # I.e. 3 different areas in Stockholm.
    # 
    # These projects are given by the assignment for the course.
    # In order to do a Real Estate Market Analysis (REMA) we need
    # one (1) refrence project and two (2) others that we can compare.
    #
    # The projects are three different OBJECTS.
    # The classes can be found in the beginnning

    a = createProjectA()
    b = createProjectB()
    c = createProjectC()

    # List containing all the objects
    # The script loops trought each item in the list.
    projects = [a,b,c]

    # === LOAD SETTINGS ===
    # 
    # Are set in the beginning of this file (!)
    #   geoDist = distance in meters from the project's coordinates
    #   self.tradeMaxCount = how many results that will be shown.

    settings = createSettings()

    # ==== LOAD COMPANIES ===
    #
    # Load companies ID from a CSV file.
    # The IDs are used to idenfiy the industry of the company
    compIDs = getCompIDs()

    # === GET DATA ===
    #
    # Creates a HTTP GET Response

    response = getData(user, projects, compIDs,settings)

    # === GET DATA ===
    # 
    # Writes the response to a (clear) CSV file
    writeSomething(response)

    # === DONE ===
    print "\nScrip done. Shutting down..."
    quit()

if __name__ == "__main__":
    main()

