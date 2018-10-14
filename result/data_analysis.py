import matplotlib.pyplot as plt
import functools
applications=['drill','hdfs','hive','mapreduce','pig','spark','storm','yarn','hbase']
namefile="cross_application_configuration_new.txt"
def configuration_document_distribution():
	f=open(namefile,'r')
	document={}
	for line in f:
		content=line.split()
		if content[2] not in document:
			document[content[2]]=[]
			document[content[2]].append(content[0])
			document[content[2]].append(content[1])
		else:
			if content[0] not in document[content[2]]:
				document[content[2]].append(content[0])
			if content[1] not in document[content[2]]:
				document[content[2]].append(content[1])
	statistics={}
	for docu in document:
		number=len(document[docu])
		if number not in statistics:
			statistics[number]=1
		else:
			statistics[number]+=1
	x=[]
	y=[]
	for key in statistics:
		x.append(statistics[key])
		y.append(key)
	plt.plot(x,y,'*')
	plt.xlabel("Number of documents")
	plt.ylabel("Number of configurations in each document")
	plt.show()
def study_of_each_application():
	f=open(namefile,'r')
	configurations={}
	occur={}
	result={}
	for app in applications:
		configurations[app]=[]
		result[app]=0
		f_two=open("../"+app+"-configuration",'r')
		for line in f_two:
			name=line.split("**")[0].strip()
			name=app+":"+name
			configurations[app].append(name)
	for line in f:
		content=line.split()
		if content[0] in occur:
			continue
		else:
			occur[content[0]]=1
			flag=0
			for app in applications:
				if flag==1:
					break
				for config in configurations[app]:
					if config==content[0]:
						result[app]+=1
						flag=1
						break
		if content[1] in occur:
			continue
		else:
			occur[content[1]]=1
			flag=0
			for app in applications:
				if flag==1:
					break
				for config in configurations[app]:
					if config==content[1]:
						result[app]+=1
						flag=1
						break
	for app in applications:
		print app,len(configurations[app]), result[app]
def C_n(n):
	return (n-1)*n/2
def compute_score(content):
	result=0.
	for n in content:
		result+=1./C_n(n)
	return result
def cross_relations_among_configurations():
	f=open(namefile,'r')
	document={}
	for line in f:
		content=line.split()
		if content[2] not in document:
			document[content[2]]=[]
			document[content[2]].append(content[0])
			document[content[2]].append(content[1])
		else:
			if content[0] not in document[content[2]]:
				document[content[2]].append(content[0])
			if content[1] not in document[content[2]]:
				document[content[2]].append(content[1])
	f.close()

	f=open(namefile,'r')
	f_out=open("result.txt",'w')
	statistics={}
	score={}
	for line in f:
		content=line.split()
		if content[0]<content[1]:
			content[1],content[0]=content[0],content[1]
		key=content[0]+' '+content[1]
		if key not in statistics:
			statistics[key]=[]
			statistics[key].append(len(document[content[2]]))
		else:
			statistics[key].append(len(document[content[2]]))
	for key in statistics:
		score[key]=compute_score(statistics[key])
	result=[]
	for key in statistics:
		result.append(key)
	for i in range(len(result)-1,0,-1):
		for j in range(i,0,-1):
			if score[result[j]]>score[result[j-1]]:
				result[j],result[j-1]=result[j-1],result[j]
	for i in range(len(result)):
		f_out.write(result[i]+' scores:'+str(score[result[i]])+'\n')
	f_out.close()
	f.close()
#configuration_document_distribution()
#study_of_each_application()
#cross_relations_among_configurations()