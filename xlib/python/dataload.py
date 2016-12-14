"""
Form data file to data
"""
import os
import numpy
class floatdata:
	def load(self,path):
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
