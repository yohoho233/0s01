#!/usr/bin/python
#coding=utf-8
# Import modules for CGI handling
import cgi, os
import cgitb; cgitb.enable()
import os
import os.path


#import facedetectme
form = cgi.FieldStorage()
# Get filename here.
try:
	fileitem = form['up_file']
	# Test if the file was uploaded
	if fileitem.filename:
		fn = os.path.basename(fileitem.filename)
		open('/home/xhq/lab_web/Upload/' + fn, 'wb').write(fileitem.file.read())
		message = 'The file "' + fn + '" was uploaded successfully'
	else:
		message = 'No file was uploaded'
except:
	message='index'
rootdir = '/home/xhq/lab_web/Upload'

str_files="""Change the name of PPT as date+your-name  e.g.<font color="blue"> 20161204Luffy.pptx</font><hr/>"""
for parent,dirnames,filenames in os.walk(rootdir):
	
	for filename_t in filenames:
		filename=''
		for i in filename_t:
			if i==' ':
				filename+='%20'
			else:
				filename+=i
		filelink='<a href=http://114.55.145.9:2334/Upload/'+filename+'>'+filename_t+'</a><br>'
		str_files=str_files+filelink
		#str_files=str_files+filename+'<br/>'

sstr="""\
	 Content-Type: text/html\n

	 <html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>Submit Files</title><style type="text/css"></style></head><body><br>
	<h1 style="text-align: center" class="first">Submit Files<br></h1>
	<form action="uploadserver.py" method="post" enctype="multipart/form-data">
	<input type="submit" name="submit" value="Submit Files" /> <a > <a/> <input name="up_file" type="file" name="file" id="file" /><br></form>
%s
</body><div></div></html>
"""%(str_files)
print sstr
