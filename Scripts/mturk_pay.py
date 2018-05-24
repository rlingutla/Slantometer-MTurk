"""Script pays all mturk workers who have completed HITs.
Script extracts HIT IDs from a list of files and associated IDs. 
Mturk Approve Assigment function is used pay subjects via ID."""

import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import HTMLQuestion 
import csv 
import json
import os
from operator import itemgetter
from variables import aws_access_key, aws_secret_key, host, form, result

# Create your connection to MTurk
mtc = MTurkConnection(aws_access_key_id=aws_access_key,
aws_secret_access_key=aws_secret_key,
host=host) 

infile_control = 'mturk_hit_Ids_need_payment.txt'

control = []
with open(infile_control) as f:
	control = f.read().splitlines()

for item in control: 
	line = item.split(',') 
	if(len(line) > 1):
		hit_id = line[-1]  
		print(hit_id)
		try:
			result = mtc.get_assignments(hit_id) 
			for r in result: 
				print(r.AssignmentId) 
				try:
					mtc.approve_assignment(r.AssignmentId)
				except: 
					print('')
		except:
			print('HIT ID is no longer available')