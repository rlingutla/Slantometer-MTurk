import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import HTMLQuestion 
import csv 
import json
import os
from operator import itemgetter
total_sentences = 0
from variables import aws_access_key, aws_secret_key, host, form, result

# Connection to MTurk
mtc = MTurkConnection(aws_access_key_id=aws_access_key,
aws_secret_access_key=aws_secret_key,
host=host)

if __name__ == '__main__':
	infile_one = '../data/response_ids.csv' 
	infile_two = 'mturk_hit_ids_need_payment.txt'

	tested_file_names = []
	with open(infile_one) as f:
		lines = f.read().splitlines()
		for l in lines:
			tested_file_names.append(l[1:-1])

	with open(infile_two) as f:
		additional_lines = f.read().splitlines()
		for al in additional_lines:
			tested_file_names.append(al)

	worker_ids = []
	responses = dict()

	#for each file
	for item in tested_file_names:
		line = item.split(',')  
		hit_id = line[-1]
		date = line[0]
		result = mtc.get_assignments(hit_id) #for each hit ID

		try:
			assignment = result[0]
			worker_id = assignment.WorkerId 
			answers=[]
			ans = []
			for r in result: #for every response
				assignment = r
				worker_id = assignment.WorkerId 
				worker_ids.append((worker_id,line)) #keep track of worker and file 
				ans = [worker_id]
				for answer in assignment.answers[0]:
					ans += answer.fields 
				if date in responses.keys(): 
					data = responses[date]
					data.append(ans)
					responses[date] = data
				else:
					responses[date] = [ans]
				ans = [] 
		except BaseException as e:
			print(line, e)
	with open('../data/raw_data.csv', 'w') as csv_file:
	    writer = csv.writer(csv_file)
	    for key, value in responses.items():
	       writer.writerow([key, list(value)])
	for key in responses.keys():
	 	print(key, len(responses[key]))

	
	