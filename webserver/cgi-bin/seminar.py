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
       
def timeget():
        weburl='http://time.tianqi.com/'
        response=urllib.urlopen(weburl)
        lines=response.read()

        reg = r'\d\d:\d\d:\d\d'
        pattern=re.compile(reg)
        com=re.compile(reg)
        url= re.findall(pattern,lines)
        return  url[0]

#Date get
time_str=dateget();
today_str=time_str;
stmp=time_str.split('-')
year=2016
month=int(stmp[1])
day=int(stmp[2])
#month=9
#day=16

#Data get
file=open('/data/labweb/seminar.data','r')
str_abstract='<br>'
sstr=file.readlines()
date=''
flag_read=0
speakers=''
week=''
clock='13:30'
seminar_date_year='2016'
seminar_date_month=''
seminar_date_day=''
for line in sstr:
	strline=line.split("#")
	if strline[0]=='date':
		if flag_read==1:
			break
		retstring=strline[1]
		stmp=retstring.split('.')
		if int(stmp[0])<month:
			continue
		if int(stmp[0])==month and int(stmp[1])<day:
			continue
		seminar_date_month=stmp[0]
		seminar_date_day=stmp[1]
		notice_str=''
		#print seminar_date_year
		#print seminar_date_month
		#print seminar_date_day
		if os.path.exists('/data/labweb/'+seminar_date_year+seminar_date_month+seminar_date_day+'.notice'):
			notice_address_str=''
			notice_time_str=''
			notice_speaker_str=''
			notice_abstract_str=''
			file_tmp=open('/data/labweb/'+seminar_date_year+seminar_date_month+seminar_date_day+'.notice')
			tmp_str=file_tmp.readlines()
			for notice_line in tmp_str:
				notice_tmp=notice_line.split('#')
				#print notice_tmp
				if notice_tmp[0]=='address':
					notice_address_str=notice_tmp[1]	
				if notice_tmp[0]=='time':
					notice_time_str=notice_tmp[1]	
				if notice_tmp[0]=='speaker':
					notice_speaker_str=notice_tmp[1]	
				if notice_tmp[0]=='abstract':
					notice_abstract_str=notice_tmp[1]	
			notice_str="""<td width="50%%"><b><p></p><font color="blue"><p></p>Address: %s<br><p></p>Date: %s<br><p></p>Speaker: %s<br><p></p>Abstract: %s<br></font></b></td>"""%(notice_address_str,notice_time_str,notice_speaker_str,notice_abstract_str)
		try:
			week=strline[2]
		except:
			week='Saturday'
		try:
			clock=strline[3]
		except:
			clock='13:30'
		flag_read=1
		date="%02d"%int(stmp[0])+'.'+"%02d"%int(stmp[1])
		continue
	if flag_read==1:
		stmp=line.split('#')
		name=stmp[0]
		speakers=speakers+name+' / '
		title=stmp[1]
		paper=stmp[2]
		try:
			abstract_str=stmp[3]
		except:
			abstract_str='Searching abstract...'
		try:
			link_str=stmp[4]
		except:
			link_str=paper+'/'+title+'.pdf'
		
		str_abstract_tmp="""
<hr><b>Title:</b> %s <br><b>Date:</b> 2016.%s <br><b>Speaker:</b> %s <br><b>Abstract:</b><br><div style="text-align:justify"> %s</div>
<b>Paper:</b> %s<a href="http://114.55.145.9:8080/References/seminar/%s">[PDF]</a> <br>
"""%(title,date,name,abstract_str,paper,link_str)

		str_abstract=str_abstract+str_abstract_tmp

str_where="""<b>WHERE: Room 511, GuangZhi-C Buliding (Pingfeng campus)</b><p></p><b>WHEN: %s,%s, 2016.%s</b> <p></p><b>Speaker(s):  %s </b><br></td>"""%(clock,week,date,speakers)
#str_where="""<b>WHERE: Room 108, GuangZhi-B Buliding (Pingfeng campus)</b><p></p><b>WHEN: %s,%s, 2016.%s</b> <p></p><b>Speaker(s):  %s </b><br></td>"""%(clock,week,date,speakers)

sstr="""\
	 Content-Type: text/html\n

<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>Group Seminar </title><style type="text/css">
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
	</style></head>
	<body style="font-family: 'Open Sans', Helvetica, Arial, sans-serif;font-size: 15px;font-weight: 300;"><p></p><h1 style="text-align: center" class="first">Group Seminar</h1><br>Today is %s<br><a href="uploadserver.py">[Submit files]</a><hr>
	<h1 style="text-align: left" class="first">Seminar Notification</h1>
	<h2><b><a href="http://114.55.145.9:2334/cgi-bin/seminarplan.py">Semester Schedule</a> (Updated on: 2016.11.03)</b></h2>
	<table style="width:100%%"><tbody>
<tr><td><p></p>
<b>Intelligent Vision &amp; Social Network</b><p></p>
%s%s</tr></tbody></table>%s
<hr><!--Previous Seminars-->		
<h2>Previous Seminars </h2>	
<a href="http://114.55.145.9:2334/cgi-bin/previous.py">[2016.09-]</a><br>
<hr>
<!--Materials-->	
<h2>Materials</h2>
<!--AAAI2016------------------------------------------------------------------------------->
<h3>AAAI2016</h3>
<a href="http://114.55.145.9:8080/References/seminar/AAAI2016/Analyzing%%20NIH%%20Funding%%20Patterns%%20over%%20Time%%20with%%20Statistical%%20Text%%20Analysis.pdf">Analyzing NIH Funding Patterns over Time with Statistical Text Analysis.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/AAAI2016/Automatically%%20Augmenting%%20Titles%%20of%%20Research%%20Papers%%20for%%20Better%%20Discovery.pdf">Automatically Augmenting Titles of Research Papers for Better Discovery.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/AAAI2016/Automatic%%20Summary%%20Generation%%20for%%20Scientific%%20Data%%20Charts.pdf">Automatic Summary Generation for Scientific Data Charts.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/AAAI2016/Discovering%%20Relevant%%20Hashtags%%20for%%20Health%%20Concepts%%20A%%20Case%%20Study%%20of%%20Twitter.pdf">Discovering Relevant Hashtags for Health Concepts A Case Study of Twitter.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/AAAI2016/From%%20a%%20Scholarly%%20Big%%20Dataset%%20to%%20a%%20Test%%20Collection%%20for%%20Bibliographic%%20Citation%%20Recommendation.pdf">From a Scholarly Big Dataset to a Test Collection for Bibliographic Citation Recommendation.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/AAAI2016/Modeling%%20Topic-Level%%20Academic%%20Influence%%20in%%20Scientific%%20Literatures.pdf">Modeling Topic-Level Academic Influence in Scientific Literatures.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/AAAI2016/Venting%%20Weight%%20Analyzing%%20the%%20Discourse%%20of%%20an%%20Online%%20Weight%%20Loss%%20Forum.pdf">Venting Weight Analyzing the Discourse of an Online Weight Loss Forum.pdf</a><br>
<h3>CVPR2016</h3>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Detecting%%20events%%20and%%20key%%20actors%%20in%%20multi-person%%20videos.pdf">Detecting events and key actors in multi-person videos.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/DeepFashion%%20Powering%%20Robust%%20Clothes%%20Recognition%%20and%%20Retrieval%%20with%%20rich%%20annotations.pdf">DeepFashion Powering Robust Clothes Recognition and Retrieval with rich annotations.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Deep%%20Residual%%20Learning%%20for%%20Image%%20Recognition.pdf">Deep Residual Learning for Image Recognition.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Embedding%%20Label%%20Structures%%20for%%20Fine-Grained%%20Feature%%20Representation.pdf">Embedding Label Structures for Fine-Grained Feature Representation.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Equiangular%%20Kernel%%20Dictionary%%20Learning%%20with%%20Applications%%20to%%20Dynamic%%20Texture%%20Analysis.pdf">Equiangular Kernel Dictionary Learning with Applications to Dynamic Texture Analysis.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Fine-grained%%20Image%%20Classification%%20by%%20Exploring%%20Bipartite-Graph%%20Labels.pdf">Fine-grained Image Classification by Exploring Bipartite-Graph Labels.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/HD%%20Maps%%20Fine-grained%%20Road%%20Segmentation%%20by%%20Parsing%%20Ground%%20and%%20Aerial%%20Images.pdf">HD Maps Fine-grained Road Segmentation by Parsing Ground and Aerial Images.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Image%%20Question%%20Answering%%20using%%20Convolutional%%20Neural%%20Network%%20with%%20Dynamic%%20Parameter%%20Prediction.pdf">Image Question Answering using Convolutional Neural Network with Dynamic Parameter Prediction.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Learning%%20Deep%%20Representations%%20of%%20Fine-Grained%%20Visual%%20Descriptions.pdf">Learning Deep Representations of Fine-Grained Visual Descriptions.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Object%%20Skeleton%%20Extraction%%20in%%20Natural%%20Images%%20by%%20Fusing%%20Scale-associated%%20Deep%%20Side%%20Outputs.pdf">Object Skeleton Extraction in Natural Images by Fusing Scale-associated Deep Side Outputs.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Part-Stacked%%20CNN%%20for%%20Fine-Grained%%20Visual%%20Categorization.pdf">Part-Stacked CNN for Fine-Grained Visual Categorization.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Picking%%20Deep%%20Filter%%20Responses%%20for%%20Fine-grained%%20Image%%20Recognition.pdf">Picking Deep Filter Responses for Fine-grained Image Recognition.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/SketchNet%%20Sketch%%20Classification%%20with%%20Web%%20Images.pdf">SketchNet: Sketch Classification with Web Images.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Sparse%%20Coding%%20for%%20Third-order%%20Super-symmetric%%20Tensor%%20Descriptors%%20with%%20Application%%20to%%20Texture%%20Recognition.pdf">Sparse Coding for Third-order Super-symmetric Tensor Descriptors with Application to Texture Recognition.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/SPDA-CNN_%%20Unifying%%20Semantic%%20Part%%20Detection%%20and%%20Abstraction%%20for%%20Fine-grained%%20Recognition.pdf">SPDA-CNN_ Unifying Semantic Part Detection and Abstraction for Fine-grained Recognition.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Stacked%%20Attention%%20Networks%%20for%%20Image%%20Question%%20Answering.pdf">Stacked Attention Networks for Image Question Answering.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Video%%20Segmentation%%20via%%20Object%%20Flow.pdf">Video Segmentation via Object Flow.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/Visualizing%%20and%%20Understanding%%20Deep%%20Texture%%20Representations.pdf">Visualizing and Understanding Deep Texture Representations.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/CVPR2016/You%%20Only%%20Look%%20Once_%%20Unified,%%20Real-Time%%20Object%%20Detection.pdf">You Only Look Once_ Unified, Real-Time Object Detection.pdf</a><br>
<!--ISCE2016---------------------------------------------------------------------------->
<h3>ICSE2016</h3>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/AntMiner%%20Mining%%20More%%20Bugs%%20by%%20Reducing%%20Noise%%20Interference.pdf">AntMiner Mining More Bugs by Reducing Noise Interference.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/Automated%%20Parameter%%20Optimization%%20of%%20Classification%%20Techniques%%20for%%20Defect%%20Prediction%%20Models.pdf">Automated Parameter Optimization of Classification Techniques for Defect Prediction Models.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/Automatically%%20Learning%%20Semantic%%20Features%%20for%%20Defect%%20Prediction.pdf">Automatically Learning Semantic Features for Defect Prediction.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/Belief%%20&amp;%%20Evidence%%20in%%20Empirical%%20Software%%20Engineering.pdf">Belief &amp; Evidence in Empirical Software Engineering.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/Building%%20a%%20Theory%%20of%%20Job%%20Rotation%%20in%%20Software%%20Engineering%%20from%%20an%%20Instrumental%%20Case%%20Study.pdf">Building a Theory of Job Rotation in Software Engineering from an Instrumental Case Study.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/Code%%20Review%%20Quality%%20How%%20Developers%%20See%%20It.pdf">Code Review Quality How Developers See It.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/Inflow%%20and%%20Retention%%20in%%20OSS%%20Communities%%20with%%20Commercial%%20involvement%%20A%%20Case%%20Study%%20of%%20Three%%20Hybrid%%20Projects.pdf">Inflow and Retention in OSS Communities with Commercial involvement A Case Study of Three Hybrid Projects.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/Overcoming%%20Open%%20Source%%20Project%%20Entry%%20Barriers%%20with%%20a%%20Portal%%20for%%20Newcomers.pdf">Overcoming Open Source Project Entry Barriers with a Portal for Newcomers.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/Revisiting%%20Code%%20Ownership%%20and%%20its%%20Relationship%%20with%%20Software%%20Quality%%20in%%20the%%20Scope%%20of%%20Modern%%20Code%%20Review.pdf">Revisiting Code Ownership and its Relationship with Software Quality in the Scope of Modern Code Review.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/The%%20Challenges%%20of%%20Staying%%20Together%%20While%%20Moving%%20Fast%%20An%%20Exploratory%%20Study.pdf">The Challenges of Staying Together While Moving Fast An Exploratory Study.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/ICSE2016/The%%20Emerging%%20Role%%20of%%20Data%%20Scientists%%20on%%20Software%%20Development%%20Teams.pdf">The Emerging Role of Data Scientists on Software Development Teams.pdf</a><br>
<!--KDD2016---------------------------------------------------------------------------->	
<h3>KDD2016</h3>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/A%%20Multi-Task%%20Learning%%20Formulation%%20for%%20Survival%%20Analysis.pdf">A Multi-Task Learning Formulation for Survival Analysis.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Anomaly%%20Detection%%20Using%%20Program%%20Control%%20Flow%%20Graph%%20Mining%%20from%%20Execution%%20Logs.pdf">Anomaly Detection Using Program Control Flow Graph Mining from Execution Logs.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Approximate%%20Personalized%%20PageRank%%20on%%20Dynamic%%20Graphs.pdf">Approximate Personalized PageRank on Dynamic Graphs.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/A%%20Subsequence%%20Interleaving%%20Model%%20for%%20Sequential%%20Pattern%%20Mining.pdf">A Subsequence Interleaving Model for Sequential Pattern Mining.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Come-and-Go%%20Patterns%%20of%%20Group%%20Evolution%%20A%%20Dynamic%%20Model.pdf">Come-and-Go Patterns of Group Evolution A Dynamic Model.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/DeepIntent%%20Learning%%20Attentions%%20for%%20Online%%20Advertising.pdf">DeepIntent Learning Attentions for Online Advertising.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/GMove%%20Group-Level%%20Mobility%%20Modeling%%20Using%%20Geo-Tagged%%20Social%%20Media.pdf">GMove Group-Level Mobility Modeling Using Geo-Tagged Social Media.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Inferring%%20Network%%20Effects%%20from%%20Observational%%20Data.pdf">Inferring Network Effects from Observational Data.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Large-Scale%%20Item%%20Categorization%%20in%%20e-Commerce%%20Using%%20Multiple%%20Recurrent%%20Neural%%20Networks.pdf">Large-Scale Item Categorization in e-Commerce Using Multiple Recurrent Neural Networks.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Lexis%%20An%%20Optimization%%20Framework%%20for%%20Discovering%%20the%%20Hierarchical%%20Structure%%20of%%20Sequential%%20Data.pdf">Lexis An Optimization Framework for Discovering the Hierarchical Structure of Sequential Data.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Mining%%20Subgroups%%20with%%20Exceptional%%20Transition%%20Behavior.pdf">Mining Subgroups with Exceptional Transition Behavior.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/node2vec%%20Scalable%%20Feature%%20Learning%%20for%%20Networks.pdf">node2vec Scalable Feature Learning for Networks.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Point-of-Interest%%20Recommendations%%20Learning%%20Potential%%20Check-ins%%20from%%20Friends.pdf">Point-of-Interest Recommendations Learning Potential Check-ins from Friends.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Ranking%%20Relevance%%20in%%20Yahoo%%20Search.pdf">Ranking Relevance in Yahoo Search.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Robust%%20Extreme%%20Multi-label%%20Learning.pdf">Robust Extreme Multi-label Learning.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Smart%%20Reply%%20Automated%%20Response%%20Suggestion%%20for%%20Email.pdf">Smart Reply Automated Response Suggestion for Email.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Structural%%20Neighborhood%%20Based%%20Classification%%20of%%20Nodes%%20in%%20a%%20Network.pdf">Structural Neighborhood Based Classification of Nodes in a Network.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Taxi%%20Driving%%20Behavior%%20Analysis%%20in%%20Latent%%20Vehicle-to-Vehicle%%20Networks%%20A%%20Social%%20Influence%%20Perspective.pdf">Taxi Driving Behavior Analysis in Latent Vehicle-to-Vehicle Networks A Social Influence Perspective.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Transfer%%20Knowledge%%20between%%20Cities.pdf">Transfer Knowledge between Cities.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/When%%20Social%%20Influence%%20Meets%%20Item%%20Inference.pdf">When Social Influence Meets Item Inference.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/KDD2016/Why%%20Should%%20I%%20Trust%%20You%%20Explain%%20the%%20Predictions%%20of%%20Any%%20Classifier.pdf">Why Should I Trust You Explain the Predictions of Any Classifier.pdf</a><br>
<!--WWW016---------------------------------------------------------------------------->
<h3>WWW2016</h3>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Addressing%%20Complex%%20and%%20Subjective%%20Product-Related%%20Queries%%20with%%20customer%%20Reviews.pdf">Addressing Complex and Subjective Product-Related Queries with customer Reviews.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Beyond%%20Collaborative%%20Filtering%%20The%%20List%%20Recommendation%%20Problem.pdf">Beyond Collaborative Filtering The List Recommendation Problem.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Exploiting%%20Dining%%20Preference%%20for%%20Restaurant%%20Recommendation.pdf">Exploiting Dining Preference for Restaurant Recommendation.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Exploring%%20Limits%%20to%%20Prediction%%20in%%20Complex%%20Social%%20Systems.pdf">Exploring Limits to Prediction in Complex Social Systems.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Gender%%20Productivity%%20and%%20Prestige%%20in%%20Computer%%20Science%%20Faculty%%20Hiring%%20Networks.pdf">Gender Productivity and Prestige in Computer Science Faculty Hiring Networks.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/HeteroSales%%20Utilizing%%20Heterogeneous%%20Social%%20Networks%%20to%%20Identify%%20the%%20Next%%20Enterprise%%20Customer.pdf">HeteroSales Utilizing Heterogeneous Social Networks to Identify the Next Enterprise Customer.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Immersive%%20Recommendation%%20News%%20and%%20Event%%20recommendations%%20Using%%20Personal%%20Digital%%20Traces.pdf">Immersive Recommendation News and Event recommendations Using Personal Digital Traces.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Linking%%20Users%%20Across%%20Domains%%20with%%20Location%%20Data%%20Theory%%20and%%20validation.pdf">Linking Users Across Domains with Location Data Theory and validation.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Measuring%%20Urban%%20Social%%20Diversity%%20Using%%20Interconnected%%20Geo-Social%%20Networks.pdf">Measuring Urban Social Diversity Using Interconnected Geo-Social Networks.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Mining%%20Online%%20Social%%20Data%%20for%%20Detecting%%20Social%%20Network%%20Mental%%20Disorders.pdf">Mining Online Social Data for Detecting Social Network Mental Disorders.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Modeling%%20User%%20Consumption%%20Sequences.pdf">Modeling User Consumption Sequences.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Modeling%%20User%%20Exposure%%20in%%20Recommendation.pdf">Modeling User Exposure in Recommendation.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/On%%20Sampling%%20Nodes%%20in%%20a%%20Network.pdf">On Sampling Nodes in a Network.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Recommendations%%20in%%20Signed%%20Social%%20Networks.pdf">Recommendations in Signed Social Networks.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Social%%20Networks%%20Under%%20Stress.pdf">Social Networks Under Stress.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Table%%20Cell%%20Search%%20for%%20Question%%20Answering.pdf">Table Cell Search for Question Answering.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/The%%20Effect%%20of%%20Recommendations%%20on%%20Network%%20Structure.pdf">The Effect of Recommendations on Network Structure.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/The%%20Lifecycle%%20and%%20Cascade%%20of%%20WeChat%%20Social%%20Messaging%%20Groups.pdf">The Lifecycle and Cascade of WeChat Social Messaging Groups.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/TribeFlow%%20Mining%%20&amp;%%20Predicting%%20User%%20Trajectories.pdf">TribeFlow Mining &amp; Predicting User Trajectories.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Ups%%20and%%20Downs%%20Modeling%%20the%%20Visual%%20Evolution%%20of%%20Fashion%%20Trends%%20with%%20One-Class%%20Collaborative%%20Filtering.pdf">Ups and Downs Modeling the Visual Evolution of Fashion Trends with One-Class Collaborative Filtering.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/Using%%20Shortlists%%20to%%20Support%%20Decision%%20Making%%20and%%20Improve%%20Recommender%%20System%%20Performance.pdf">Using Shortlists to Support Decision Making and Improve Recommender System Performance.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/What%%20links%%20Alice%%20and%%20Bob%%20Matching%%20and%%20Ranking%%20Semantic%%20Patterns%%20in%%20Heterogeneous%%20Networks.pdf">What links Alice and Bob Matching and Ranking Semantic Patterns in Heterogeneous Networks.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/WWW2016/When%%20do%%20Recommender%%20Systems%%20Work%%20the%%20Best.pdf">When do Recommender Systems Work the Best.pdf</a><br>
<!--Nature & Science & PNAS--------------------------------------------------------------------------->
<h3>Nature &amp; Science &amp; PNAS</h3>
<a href="http://114.55.145.9:8080/References/seminar/PNAS/Unfolding%%20large-scale%%20online%%20collaborative%%20human%%20dynamics.pdf">Unfolding large-scale online collaborative human dynamics</a><br>
<a href="http://114.55.145.9:8080/References/seminar/PNAS-2015-Dodds-2389-94.pdf">Human language reveals a universal positivity bias.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/PNAS-2015-L-2325-30.pdf">Toward link predictability of complex networks.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/PNAS-2015-Wasserman-1281-6.pdf">Cross-evaluation of metrics to estimate the significance of creative works.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/nature14604.pdf">Influence maximization in complex networks through optimal percolation.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/e1501742.full.pdf">Women\'s connectivity in extreme networks.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/163.full.pdf">Higher-order organization of complex networks.pdf</a><br>
<!--Other Sources--------------------------------------------------------------------------->
<h3>Other Sources</h3>
<a href="http://114.55.145.9:8080/References/seminar/Generation%%20and%%20Comprehension%%20of%%20Unambiguous%%20Object%%20Descriptions.pdf">Generation and Comprehension of Unambiguous Object Descriptions.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/TI-POOLING_%%20transformation-invariant%%20pooling%%20for%%20feature%%20learning%%20in%%20Convolutional%%20Neural%%20Networks.pdf">TI-POOLING: transformation-invariant pooling for feature learning in Convolutional Neural Networks
.pdf</a><br>
<a href="http://114.55.145.9:8080/References/seminar/srep32502.pdf">Serving by local consensus in the public service location game.pdf</a><br>
<a href="http://114.55.145.9:8080/References/netsci/1608.06949v1.pdf">Urban Pulse: Capturing the Rhythm of Cities.pdf</a><br>
<p></p>
<hr>
<div id="footer" style="text-align: center">Internal Information &copy 2016 IVSN Group</div><div></div></body></html>
"""%(today_str,str_where,notice_str,str_abstract)

print sstr
