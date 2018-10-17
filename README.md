# AI2102 Project Work
KTH Royal Institute of Technology<br /> 
AI2102<br />
Project work<br />
Group D4<br />

Created by André "MG" Wisén<br />

# Intro
This is a Python Scipt used in my project work in the course AI2102.

In short: The Script is suppose to gather data for a Real Estate Market Analysis (REMA) 
The data should be of the character that it can be used in a productivity analysis. 

The project utilizes Python 2.7 and Hitta.se's REST API.

# A word on the programming
This is not the most elegant code in the world.
However, it works for me.

This can easily be done within a web browser instead. 
But I used Python instead (don't ask me why...)

# API
READ MORE: https://www.hitta.se/api (in Swedish)

# Authentication
You need a Caller ID and API Key to run this script.
The script will run without a correct one, but will only output an empty file.

READ MORE: http://hitta.github.io/public/http-api/authentication.html (in Swedish)

# How the script works
There are three different projects.<br />
One reference project and two that we compare it to.

The projects are areas in Stockholm, Sweden.<br />
The names and coordinates (based on RT90) are set in the main.py file.

The script goes through each project and finds companies based on a certain type of industry and radius.

For example (Project, Company, Distance):

Dalenum, LloydsApotek, 766.650507076<br />
Dalenum,	Kronans Apotek, 785.993638651<br />
Dalenum, Olika Teknik och Utveckling Lidingö AB, 481.11613319<br />
Dalenum, Renst Bil i Lidingö AB, 1532.62682999<br />
Dalenum, Gz Racing, 1559.97852549<br />
Dalenum, Lidingö Motorservice AB, 1577.12174546<br />
 
# Tutorial
Clone the GIT and edit the main.py file. <br />
You need to make changes to the first two classes.

1. Change the settings to your liking.
2. Fill in your Caller ID and API Key

Before you run the program, change the CSV file.<br />
Add the IDs you like to get data from, based on this list:<br />
http://hitta.github.io/public/http-api/search/tradeids.html

NOTE: The CSV is in Swedish...

Run the script via command line or via your favorite IDE.

In Terminal: python main.py<br />

The script will output a semi-comma CSV file. <br />
Import it, preferably by Excel, and use the data to make a Productivity Analysis.

# Contact
Feel free to contact me via mail if you have any questions. <br />
Yes, I speak Swedish :P

Mail: kontakt@andrewisen.se <br />
Website: http://www.andrewisen.se <br />
