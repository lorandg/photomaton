#!/usr/bin/env python
# -*- coding: utf-8 -*

import glob
import os
from os import environ
# import cgi 
import cgitb
cgitb.enable()

queryString=query = os.environ[ "QUERY_STRING" ]
     
cookies = dict()
 
if environ.has_key('HTTP_COOKIE') and environ['HTTP_COOKIE'] :
    cookies = {key:value for (key,value) in (prop.split('=') for prop in environ['HTTP_COOKIE'].split(';'))}
                
currentPicture = cookies.get("currentPicture", "")
 
files = filter(os.path.isfile, glob.glob("img/*.jpg"))
files.sort(key=lambda picture: os.path.getmtime(picture))
 
if not currentPicture :
    # display the newest picture
    currentPicture = files[-1]

curIdx = files.index(currentPicture)
 
if "next" in queryString :
    nextIdx = curIdx+1 if curIdx+1 < len(files) else 0
    currentPicture = files[nextIdx]

if "prev" in queryString :
    prevIdx = curIdx-1 if  curIdx-1 >= 0 else len(files)-1
    currentPicture = files[prevIdx]
 
cookies["currentPicture"]=currentPicture 
 
print "Set-Cookie: currentPicture = %s;" % currentPicture
print "Content-type: text/html; charset=utf-8\n"

print "<!DOCTYPE html>"
print "<head>"
print "    <title>Photomaton</title>"
print "</head>"
print "<body>"

# print "<p>files:"+str(files)+"</p>"
# print "<p>cookies:"+str(cookies)+"</p>"
# print "<p>queryString:"+queryString+"</p>"
# for param in os.environ.keys():
#    print "<b>%20s</b>: %s<\br>" % (param, os.environ[param])
# if "next" in queryString :
#     print "<p>Location: http://{0}{1}</p>".format(environ['SERVER_NAME'], environ['SCRIPT_NAME'])
#     exit(0)
   
print "<table>"
print "<tr>"
print "<td><a href=\"?prev\">previous</a>"
print "<td><a href=\"?next\">next</a>"
print "<td>"
print "<tr>"
print "</table>"

print "<ul>"

print "<img src=\""+ currentPicture +"\" height=\"50%\" width=\"50%\"\"></img>"
print "</ul>"
print "</body>"
print "</html>"
