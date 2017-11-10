#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by Andre Wisen
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

# Creates a unique user for authentication
# READ MORE: http://hitta.github.io/public/http-api/authentication.html

class createUser:
    def __init__(self):
        # Get your Caller ID and Private API Key at https://www.hitta.se/api (in Swedish)

        self.callerID = " - INSERT YOUR CALLER ID - "
        self.key =  " - INSERT YOUR PRIVATE API KEY - "


# Creates a OBJECT for each "project"
# The coordinate system is Swedish grid (RT90).
# It's an old Swedish standard, but it's the default used by hitta.se
# You can convert between RT90 and more modern ones.
# 
# Note: Outputs may be in a more modern coordinate system.

class createProjectA:
    def __init__(self):
        self.name = "Dalenum"
        self.x = 6582786
        self.y = 1633843

class createProjectB:
    def __init__(self):
        self.name = "Norra Djurgardsstaden"
        self.x = ""
        self.y = ""

class createProjectC:
    def __init__(self):
        

        self.name = "Lindingo v2 "
        self.x = ""
        self.y = ""

# Creates a temporary header
# It's temporary because the hashed string is based on Time
# (and can therefore not be re-used in other calls)
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

# Creates the base for the url OBJECT.
# This class uses methods to change the attribute

class createURL:
    def __init__(self):
        self.url = "null"

    def get(self):
        return self.url

    def set(self, url):
        self.url = url
   
def getData(user, url, headers):
    # The URL is stored as an attribute in the object URL
    path = url.url

    # HTTP GET Request
    conn = httplib.HTTPSConnection("api.hitta.se")
    conn.request("GET", path, "", headers.headers)
    resp = conn.getresponse()

    # RESPONSE
    #
    # The API will return a code that tells if the call was sucessful or not
    # 200: OK
    # 404: Error

    # print resp.status, resp.reason


    # STORE VALUES
    # 
    # The data (response) is stored as in a JSON format
    # Python handles JSON as a dictionary.
    # This code snippet stores the response in a nested dictionary

    jsonResponse = json.loads(resp.read())




    # PRINT ALL
    # 
    # Prints the whole JSON file.
    # It's a good idea to do this if you want to find out keys for the dict
    # print json.dumps(jsonResponse, indent=4, separators=(',', ': '))

    # This dictionary contains the companies names.
    compDict = jsonResponse["result"]["companies"]["company"]

    # Display all the companies names
    for eachComp in compDict:
        print eachComp["displayName"]


def setCompNear(user, project, url, tradeID, geoDist, tradeMaxCount=5):
    # repeterande separerade med komma för flera branscher
    # http://hitta.github.io/public/http-api/search/tradeids.html


    geoPoint = str(project.x) + ":" + str(project.y)
    path = "https://api.hitta.se/publicsearch/v1/companies/trade/" + str(tradeID) + "/nearby/" + str(geoPoint) + "?geo.distance=" + str(geoDist) + "&trade.max.count=" + str(tradeMaxCount)
    url.set(path)

    return url

def main():

    # === INIT === 

    # Each API Call needs authentication
    # To authenticate you need
    #   1) callerId
    #   2) private API key 
    # 
    # READ MORE (Swedish): http://hitta.github.io/public/http-api/authentication.html

    user = createUser()

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
    C = createProjectC()

    # Creates the header for the API Call
    # Each call needs a new header, since the header contains a unique hased key (based on time)

    headers = createHeader(user)

    # Creates the URL for the API Call
    # The URL is treated as a single OBJECT with an attribute that will with each call.
    url = createURL()

    # === COMPANIES WITHIN A CERTAIN INDISTRY AND RADIUS === 
    # Settings
    tradeID = 268
    geoDist = 2000
    tradeMaxCount = 10

    # Get Data
    url = setCompNear(user, a, url, tradeID, geoDist, tradeMaxCount)
    headers = createHeader(user)
    getData(user, url, headers)


if __name__ == "__main__":
    main()

