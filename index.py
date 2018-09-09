
#!/usr/bin/python3
# -*- coding: utf-8 -*

import glob
import os
from os import environ
# import cgi 
# import cgitb
# cgitb.enable()
# form = cgi.FieldStorage()
# 
# picture= form.getvalue("picture")

cookies = dict()

if environ.has_key('HTTP_COOKIE') and environ['HTTP_COOKIE'] :
    cookies = {key:value for (key,value) in (prop.split('=') for prop in environ['HTTP_COOKIE'].split(';'))}
               
currentPicture = cookies.get("currentPicture", "")

if not currentPicture :
    # display the newest picture
    files = filter(os.path.isfile, glob.glob("img/*.jpg"))
    files.sort(key=lambda picture: os.path.getmtime(picture))
    currentPicture = files[-1]
    print "Set-Cookie:currentPicture = %s;\r\n" % currentPicture 
    cookies["currentPicture"]=currentPicture 

print("Content-type: text/html; charset=utf-8\n")

print "<!DOCTYPE html>"
print "<head>"
print "    <title>Photomaton</title>"
print "<meta http-equiv=\"refresh\" content=\"1; URL=#\">"
print "</head>"
print "<body>"
# print "<p>files:"+str(files)+"</p>"
# print "<p>cookies:"+str(cookies)+"</p>"
print "<ul>"

print "<img src=\""+ currentPicture +"\" height=\"50%\" width=\"50%\"\"></img>"
print "</ul>"
print "</body>"
print "</html>"
