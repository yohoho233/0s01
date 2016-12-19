#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()
import os
import os.path
import cgi
import re
import urllib
import sys

reload(sys)
sys.setdefaultencoding('utf8')

file_head=open('/home/xhq/lab_web/cgi-bin/seminar_head.data','rb')
sstr=file_head.readlines()

head_str=sstr[0]

#Data get
file=open('/data/labweb/seminar.data','rb')
sstr=file.readlines()

str_=''
flag_notfirst=0
flag_read_firstdata=0
flag_read_nextdata=0
count=0
str_add=''

for line in sstr:
	strline=line.split("#")
	if strline[0]=='date':
		if flag_notfirst==1:
			str_add="""<tr><th  bgcolor= #efefef rowspan="%s">%s</th>"""%(str(count),date)+str_add
			str_=str_+str_add

			flag_read_firstdata=0
			str_add=''
			count=0

		flag_notfirst=1
		date_tmp=strline[1].split(".")
		date="%02d"%int(date_tmp[0])+'.'+"%02d"%int(date_tmp[1])
	else:
		count+=1
		name=strline[0]
		title=strline[1]
		paper=strline[2]

		if flag_read_firstdata==1:
			str_add=str_add+"""<tr><td bgcolor= #efefef align="center"> %s </td><td align="left" bgcolor= #efefef>%s</td><td bgcolor= #efefef align="center">%s</td></tr>"""%(name,title,paper)
		else:
			str_add=str_add+"""<td bgcolor= #efefef align="center">%s</td><td align="left" bgcolor= #efefef>%s</td><td bgcolor= #efefef align="center">%s</td></tr>"""%(name,title,paper)

		flag_read_firstdata=1

str_add="""<tr><th  bgcolor= #efefef rowspan="%s">%s</th>"""%(str(count),date)+str_add
str_=str_+str_add

sstr="""\
	 Content-Type: text/html\n
<!DOCTYPE html><html ><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="192.168.1.102:2334/files/c5.css">
<title>Group Seminar </title>
</head><body style="margin:auto;width:90%%;font-family: 'Open Sans', Helvetica, Arial, sans-serif;font-size: 15px;font-weight: 300;"><div>
%s</div><div id="maincontent" align="center"><div>
<table class="dataintable" border="1" bordercolor="black" cellspacing="0">
<tbody><tr><th bgcolor= #d5d5d5>&nbsp;Date&nbsp;</th><th bgcolor= #d5d5d5>Reader</th><th bgcolor= #d5d5d5>Title</th><th bgcolor= #d5d5d5>Paper</th></tr>
%s
</tbody></table><br></body></html>"""%(head_str,str_)

print sstr
