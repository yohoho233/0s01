#!/usr/bin/python
#coding=utf-8
# Import modules for CGI handling
import cgi, os
import cgitb; cgitb.enable()
import os
import os.path


rootdir = '/home/xhq/lab_web/debug/'
debug_str='<br>debug:'
#import facedetectme
form = cgi.FieldStorage()
# Get filename here.
fileitem = form['up_file']
#print fileitem
# Test if the file was uploaded
if fileitem.filename:
	fn = os.path.basename(fileitem.filename)
	open(rootdir + fn, 'wb').write(fileitem.file.read())
	message = 'The file "' + fn + '" was uploaded successfully'
else:
	#delete files
	try:
		debug0=form['a']
		ct=debug0.value
		for parent,dirnames,filenames in os.walk(rootdir):
        		filename=filenames[int(ct)]
			debug_str+=filename
			os.remove(rootdir+filename)
			
	except:
		message = 'No file was uploaded'

str_files=""""""
for parent,dirnames,filenames in os.walk(rootdir):
	countfile=0	
	for filename_t in filenames:
		filename=''
		for i in filename_t:
			if i==' ':
				filename+='%20'
			else:
				filename+=i
		filelink='<a href=http://114.55.145.9:2334/debug/'+filename+'>'+filename_t+'</a>'
		delete_str="""<a href=http://114.55.145.9:2334/cgi-bin/debug.py?up_file=''&a=%s>[delete]</a>"""%(str(countfile))
		str_files=str_files+filelink+'&nbsp&nbsp'+delete_str+'<br>'
		countfile+=1	
sstr="""\
	 Content-Type: text/html\n

	 <html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>Submit Files</title><style type="text/css">
article{
		-webkit-column-count: 2;
		-webkit-column-gap: 21px;
		-moz-column-count: 2;
		-moz-column-gap: 21px;
		column-count: 2;
		column-gap: 21px;
		}
	h1 {
		text-align: center;
		-webkit-column-span: all;
		-moz-column-span: all;
		column-span: all;
		}
	p {
		margin-top: 0px;
		margin-bottom: 12px;
		}
	footer{
		-webkit-column-span:all;
		-moz-column-span:all;
		column-span:all;
		}

	table,tr, td, th {
		border: 1px soild black;
		border-collapse: collapse;
		padding: 3px;
		}
	</style></head><body><br>

	<h1 style="text-align: center" class="first">Submit Files<br></h1>
	<form action="http://114.55.145.9:2334/cgi-bin/debug.py" method="post" enctype="multipart/form-data">
		<input type="submit" name="submit" value="Submit Files" /> <a > <a/> <input name="up_file" type="file" name="file" id="file" /><br>
	</form>
	
%s
%s
</body><div></div></html>
"""%(str_files,debug_str)
print sstr
