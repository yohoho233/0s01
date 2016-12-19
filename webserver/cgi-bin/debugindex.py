#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()
import os
import os.path
import cgi

rootdir = '/home/xhq/lab_web/debug'

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
sstr="""\
	 Content-Type: text/html\n

	 <html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>Submit Files</title><style type="text/css">
	</style></head><body><br>

	<h1 style="text-align: center" class="first">Submit Files<br></h1>
	<form action="debug.py" method="post" enctype="multipart/form-data">
		<input type="submit" name="submit" value="Submit Files" /> <a > <a/> <input name="up_file" type="file" name="file" id="file" /><br>
	</form>
	
%s

</body><div></div></html>
"""%(str_files)

print sstr
