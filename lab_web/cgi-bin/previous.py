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

def dateget():
        weburl='http://time.tianqi.com/'
        response=urllib.urlopen(weburl)
        lines=response.read()
        reg = r'20\d\d-\d\d-\d\d'
        pattern=re.compile(reg)
        com=re.compile(reg)
        url= re.findall(pattern,lines)
        return url[0]
#Date get
time_str=dateget();
today_str=time_str;
stmp=time_str.split('-')
year=2016
month=int(stmp[1])
day=int(stmp[2])

#Data get
file=open('/data/labweb/seminar.data','r')
str_abstract=''
sstr=file.readlines()
datecode='20160000'
date=''
flag_read=0
str_abstract_tmp=''
ulli=''
speakercode=0
datetmp=''
for line in sstr:
	strline=line.split("#")
	if strline[0]=='date':
		speakercode=0
		retstring=strline[1]
		stmp=retstring.split('.')
		datecode='2016-'+"%02d"%int(stmp[0])+'-'+"%02d"%int(stmp[1])
		datetmp=str(year)+"%02d"%int(stmp[0])+"%02d"%int(stmp[1])
		if int(stmp[0])>month:
			break
		if int(stmp[1])>day and int(stmp[0])==month:
			break
		str_abstract=str_abstract+"""</section><section id="date%s" ><h3 ><hr>Date:%s<br></h3>"""%(datecode,datecode)
		ulli=ulli+"""<li style="margin-left: 0;"><a style="color: #196d92;padding-left: 1.5rem;padding-right: 1.5rem;" href="#date%s">%s</a></li>"""%(datecode,datecode)
		
		flag_read=1
		date=stmp[0]+'.'+stmp[1]
		continue
	if flag_read==1:
		stmp=line.split('#')
		name=stmp[0] 
		#speakercode+=1
		title=stmp[1]
		paper=stmp[2]
		try:
			abstract_str=stmp[3]
		except:
			abstract_str='Searching abstract...'
		try:
			linkpdf=stmp[4]
		except:
			linkpdf=paper+'/'+title+'.pdf'
		ppttmp=datetmp+str(speakercode)+'.pptx'
		speakercode+=1
		#print '############################'+'/usr/local/apache-tomcat-8.0.35/webapps/References/seminar/PPT/'+ppttmp
		if os.path.exists('/usr/local/apache-tomcat-8.0.35/webapps/References/seminar/PPT/'+ppttmp):
			linkppt=ppttmp+"""">[PPT]"""
		else:
			ppttmp=ppttmp[0:-1]
			if os.path.exists('/usr/local/apache-tomcat-8.0.35/webapps/References/seminar/PPT/'+ppttmp):
                        	linkppt=ppttmp+"""">[PPT]"""
			else:
				ppttmp=ppttmp[0:-2]+'df'
				print 'xhq###'+'/usr/local/apache-tomcat-8.0.35/webapps/References/seminar/PPT/'+ppttmp
				if os.path.exists('/usr/local/apache-tomcat-8.0.35/webapps/References/seminar/PPT/'+ppttmp):
					linkppt=ppttmp+"""">[PPT]"""
				else:
					linkppt="""">"""
		#print '############################'+'/usr/local/apache-tomcat-8.0.35/webapps/References/seminar/PPT/'+ppttmp	
		str_abstract_tmp="""<b>Title: </b>%s<br><b>Speaker: </b>%s<br><b>Paper:</b>%s<a href="http://114.55.145.9:8080/References/seminar/%s">[PDF]</a>&nbsp;<a href="http://114.55.145.9:8080/References/seminar/PPT/%s</a><br><b>Abstract:<br> </b><div style="text-align:justify">%s</div><br>"""%(title,name,paper,linkpdf,linkppt,abstract_str)
		str_abstract=str_abstract+str_abstract_tmp

sstr="""\
	 Content-Type: text/html\n
<!DOCTYPE html><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><meta charset="utf-8"><title>Previous Seminars</title></head><body style="font-family: 'Open Sans', Helvetica, Arial, sans-serif;font-size: 15px;font-weight: 300;"><h1 style="text-align: center;">Previous Seminars</h1><div style="float: right;" ><nav style="font-size: 1.6rem;"><div style="position: fixed;top: 0;right:0;font-size: 0.75em;height: 100%% ;background-color: rgba(235, 222, 180, 0.86);"><ul><li style="margin-left: 0;"><a style="color: #196d92;padding-left: 1.5rem;padding-right: 1.5rem;" href="http://114.55.145.9:2334/cgi-bin/seminar.py">Group Seminar</a></li><br>%s<br><br>
<li style="margin-left: 0;"><a style="color: #196d92;padding-left: 1.5rem;padding-right: 1.5rem;" href="#top">Top<br><br></a></li>
<li style="margin-left: 0;"><a style="color: #196d92;padding-left: 1.5rem;padding-right: 1.5rem;" href="uploadserver.py">[Submit files]<br></a></li>
</ul></div></nav></div><div style="left:10;width:80%%"><section>%s<hr><div id="footer" style="text-align: center">Internal Information &copy 2016 IVSN Group</div></div></body></html>"""%(ulli,str_abstract)
print sstr
