r"""
used for caffe data and log
"""
import os
import numpy

class logreader:
	def readmain(self,title):
		fileio=open(title+'.log','rb')
		filetrain=open(title+'train'+'.log','wb')
		filetest=open(title+'test'+'.log','wb')

		lines=fileio.readlines()
		
		flag_get=0
		for line in lines:
			char=line.split(' ')
			line=''
			if flag_get==0:
				for i in char:
					if i=='Iteration':
						flag_get=1
						break
			if flag_get==1:
				for i in char:
					if len(i)>0:
						line+='#'+i
				char=line.split('#')
				if char[5]=='Train':
					continue
				try:
					if char[7]=='lr':
						continue
				except:
					break
				line=''
				for i in char[5:len(char)]:
					line+=' '+i
				if char[5]=='Iteration':
					if char[7]=='Testing':
						filetest.write(char[6])
					else:
						filetrain.write(char[6])
						filetrain.write(char[9])
				else:
					if char[5]=='Test':
						if char[10]=='accuracy':
							filetest.write(char[12][0:-1]+',')
						else:
							filetest.write(char[12]+'\n')
		fileio.close()
		filetrain.close()
		filetest.close()

	def dataload(self,path):
		file0=open(path)

		lines=file0.readlines()
		row=len(lines)
		line=lines[0].split(',')
		col=len(line)
		e=numpy.empty([col,row])

		countrow=0
		for line in lines:
			numstr=line.split(',')
			numstr[col-1]=numstr[col-1][0:-1]
			
			countcol=0
			for i in numstr:
				e[countcol][countrow]=float(i)
				countcol+=1
			countrow+=1
		return e