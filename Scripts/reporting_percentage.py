import sys 
import re
from itertools import groupby
from ast import literal_eval
import os
import nltk.data 
import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import HTMLQuestion 
import csv 
import json
import os
from operator import itemgetter

full_file = dict() 
event_file = dict() 
data = "../data_stats/reporting_percentage.txt"
duplicates = []

def count_lines(file,dirname):
	filename = os.fsdecode(file)
	control = [] 
	cleaned = []
	with open(dirname + filename) as f: 
		control = f.read().splitlines()
		cleaned = [x for x in control if x]
	return len(cleaned)

dirname1 = "../Official_Cleaned_files_TV_Archive/" 
dirname2 = "../Files_Done_Testing/"
for file in os.listdir(dirname1):
    filename = os.path.splitext(os.fsdecode(file))[0] 
    num_lines = count_lines(file,dirname1) 
    date = filename.split("_")[0] + "_" + filename.split("_")[1] + "_" + filename.split("_")[2] + "_" + filename.split("_")[3]
    if date in full_file.keys(): 
    	#print(date)
    	lines = full_file[date]
    	full_file[date] = lines + num_lines
    else:
    	full_file[date] = num_lines
print(len(full_file.keys()))

for file in os.listdir(dirname2):
    filename = os.path.splitext(os.fsdecode(file))[0] 
    num_lines = count_lines(file,dirname2) 
    date = filename.split("_")[0] + "_" + filename.split("_")[1] + "_" + filename.split("_")[2] + "_" + filename.split("_")[3]
    #print(date)
    if date in event_file.keys(): 
    	lines = event_file[date]
    	duplicates.append((file,num_lines))
    	event_file[date] = lines + num_lines
    else:
    	event_file[date] = num_lines 

percentages = []
for f in full_file.keys():
	if f not in event_file.keys(): 
		continue
	else: 
		percentages.append((f,str(event_file[f]/full_file[f])))



with open(data, "w") as fi:
	sorted_list = sorted(percentages, key=lambda x: x[0])
	for s in sorted_list: 
		fi.write(s[0] + ", " + s[1] + '\n')
