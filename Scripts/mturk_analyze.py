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


"""Calculate the demographic information of the workers. Function ensures that each woker is only counted once """
def demographics(people_data):
	checked_workers = [] 
	states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
	}
	gender = {'male':0,'female':0,'Other':0}
	age = {'<20':0, '20-30':0,'31-40':0,'41-50':0,'51-60':0,'61-70':0,'71+':0}
	state = dict()
	education = {'default':0,'Master': 0,'High School Diploma or Equivalent': 0,'Bachelor': 0, 'Doctoral Degree': 0, 'Associate':0}
	political_party = {'Democratic':0,'republican':0,'green':0,'Libertarian':0,'Constitution':0,'Independent':0}
	voter_status = {'yes':0, 'no':0}
	news_viewed_days = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0}
	for datum in people_data:
		if datum[0] in checked_workers:
			continue
		else:
			try:
				checked_workers.append(datum[0])
				info = datum[1]
				gender[info[1]] += 1
				age[info[0]] += 1
				education[info[3]] += 1
				political_party[info[4]] += 1
				voter_status[info[5]] += 1
				news_viewed_days[info[6]] += 1
				if info[2] in state.keys():
					state[info[2]] += 1
				else:
					state[info[2]] = 1
			except:
				continue

	"""Write the data for each demographic into a separate csv file"""
	with open('../data/gender.csv', 'w') as csv_file:
	    writer = csv.writer(csv_file)
	    for key, value in gender.items():
	       writer.writerow([key, value])
	with open('../data/age.csv', 'w') as csv_file:
	    writer = csv.writer(csv_file)
	    for key, value in age.items():
	       writer.writerow([key, value])
	with open('../data/state.csv', 'w') as csv_file:
		print(state)
		writer = csv.writer(csv_file)
		sorted_x = sorted(state.items(), key=itemgetter(1))
		sorted_x.reverse()
		for key, value in sorted_x: 
			if key == 'default':
				writer.writerow(['Unknown', value])
			else:
				writer.writerow([states[key], value])
	with open('../data/education.csv', 'w') as csv_file:
	    writer = csv.writer(csv_file)
	    for key, value in education.items():
	       writer.writerow([key, value])
	with open('../data/political_party.csv', 'w') as csv_file:
	    writer = csv.writer(csv_file)
	    for key, value in political_party.items():
	       writer.writerow([key, value])
	with open('../data/voter_status.csv', 'w') as csv_file:
	    writer = csv.writer(csv_file)
	    for key, value in voter_status.items():
	       writer.writerow([key, value])
	with open('../data/news_viewed_days.csv', 'w') as csv_file:
	    writer = csv.writer(csv_file)
	    for key, value in news_viewed_days.items():
	       writer.writerow([key, value])

"""This function is where the core of the calculations occur. The function takes in all of the worker
responses it was given and determines a label (Green or Yellow) for each sentence in the file it that was tested.
Simple statistical calculations are performed on the aggregate nubmers of the labels."""
def sort_calculate(responses, letter): 
	big_diff = 0
	little_diff = 0
	channel_date = dict()
	green_2013 = [0,0,0]
	yellow_2013 = [0,0,0]
	green_2017 = [0,0,0]
	yellow_2017 = [0,0,0]

	for key in responses.keys():
		green_tally = 0
		yellow_tally = 0
		labels = []
		for i in range(5,len(responses[key][0])): 
			green = 0
			yellow = 0
			for r in responses[key]:
				if(len(r) != 0):
					control1 = 1 if (r[0] == "'Directly discusses topic'") else 0
					control2 = .25 if (r[1] == "'Directly discusses topic'") else .75
					control3 = .1 if (r[2] == "'Directly discusses topic'") else .9
					control4 = .2 if (r[3] == "'Directly discusses topic'") else .8
					control5 = .75 if (r[4] == "'Directly discusses topic'") else .25
					control_val = sum([control1,control2,control3,control4,control5]) 
					if not (i > len(r)-1):
						if r[i] == "'Directly discusses topic'":
							green += (1*control_val)
						else:
							yellow += (1*control_val)
					else:
						continue
			if green >= yellow: 
				green_tally += 1
				labels.append('Green') 
			else:
				yellow_tally += 1
				labels.append('Yellow')

		split_key = key.split('_')
		if key[0] == '"':
			name = key[1:]
		else:
			name = key
		try:
			with open('../Tested_Broken_Files_Phase5/' + name, "r") as f:
				lines = f.read().splitlines()
				sentences = []
				#print(labels)
				i=0
				for l in lines:
					if l != '':
						if i <= 4:
							sentences.append((l,''))
						elif i > 4 and i < (len(labels) + 5):
							sentences.append((l,labels[i-5]))
						else:
							sentences.append((l,''))
						i+=1
			with open('../Sentences_With_Labels_Phase6/' + name, 'w') as csv_file:
			    writer = csv.writer(csv_file)
			    for item in sentences:
			       writer.writerow(item)

		except:
			continue

		if '2013' in split_key:
			if '"ABC' in split_key or 'ABC' in split_key:
				green_2013[0] += green_tally
				yellow_2013[0] += yellow_tally
			elif '"FOX' in split_key or 'FOX' in split_key:
				green_2013[1] += green_tally
				yellow_2013[1] += yellow_tally
			else:
				green_2013[2] += green_tally
				yellow_2013[2] += yellow_tally
		elif '2017' in split_key:
			if '"ABC' in split_key or 'ABC' in split_key:
				green_2017[0] += green_tally
				yellow_2017[0] += yellow_tally
			elif '"FOX' in split_key or 'FOX' in split_key:
				green_2017[1] += green_tally
				yellow_2017[1] += yellow_tally
			else:
				green_2017[2] += green_tally
				yellow_2017[2] += yellow_tally
		else:
			print(split_key)


		date = split_key[0] + '_' + split_key[1] + '_' + split_key[2] + '_' + split_key[3]
		if date in channel_date.keys():
			tallies = channel_date[date]
			green_tally += tallies[0]
			yellow_tally += tallies[1]
			channel_date[date] = (green_tally,yellow_tally)
		else:
			channel_date[date] = (green_tally,yellow_tally)

	if letter == 'd':
		print('Democrats:')
		print('ABC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[0]/(green_2013[0]+yellow_2013[0])*100)) + '%', ' ABC 2017 - Green Reporting: ' + str("{0:.0f}".format(green_2017[0]/(green_2017[0]+yellow_2017[0])*100)) + '%')
		print('FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[1]/(green_2013[1]+yellow_2013[1])*100)) + '%', ' FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[1]/(green_2017[1]+yellow_2017[1])*100)) + '%')
		print('NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[2]/(green_2013[2]+yellow_2013[2])*100)) + '%', ' NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[2]/(green_2017[2]+yellow_2017[2])*100)) + '%')
	elif letter == 'r':
		print('Republicans:')
		print('ABC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[0]/(green_2013[0]+yellow_2013[0])*100)) + '%', ' ABC 2017 - Green Reporting: ' + str("{0:.0f}".format(green_2017[0]/(green_2017[0]+yellow_2017[0])*100)) + '%')
		print('FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[1]/(green_2013[1]+yellow_2013[1])*100)) + '%', ' FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[1]/(green_2017[1]+yellow_2017[1])*100)) + '%')
		print('NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[2]/(green_2013[2]+yellow_2013[2])*100)) + '%', ' NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[2]/(green_2017[2]+yellow_2017[2])*100)) + '%')
	elif letter == 'o':
		print('Other:')
		print('ABC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[0]/(green_2013[0]+yellow_2013[0])*100)) + '%', ' ABC 2017 - Green Reporting: ' + str("{0:.0f}".format(green_2017[0]/(green_2017[0]+yellow_2017[0])*100)) + '%')
		print('FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[1]/(green_2013[1]+yellow_2013[1])*100)) + '%', ' FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[1]/(green_2017[1]+yellow_2017[1])*100)) + '%')
		print('NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[2]/(green_2013[2]+yellow_2013[2])*100)) + '%', ' NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[2]/(green_2017[2]+yellow_2017[2])*100)) + '%')
	elif letter == 'h':
		print('High school:')
		print('ABC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[0]/(green_2013[0]+yellow_2013[0])*100)) + '%', ' ABC 2017 - Green Reporting: ' + str("{0:.0f}".format(green_2017[0]/(green_2017[0]+yellow_2017[0])*100)) + '%')
		print('FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[1]/(green_2013[1]+yellow_2013[1])*100)) + '%', ' FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[1]/(green_2017[1]+yellow_2017[1])*100)) + '%')
		print('NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[2]/(green_2013[2]+yellow_2013[2])*100)) + '%', ' NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[2]/(green_2017[2]+yellow_2017[2])*100)) + '%')
	elif letter == 'ab':
		print('AS and BS:')
		print('ABC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[0]/(green_2013[0]+yellow_2013[0])*100)) + '%', ' ABC 2017 - Green Reporting: ' + str("{0:.0f}".format(green_2017[0]/(green_2017[0]+yellow_2017[0])*100)) + '%')
		print('FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[1]/(green_2013[1]+yellow_2013[1])*100)) + '%', ' FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[1]/(green_2017[1]+yellow_2017[1])*100)) + '%')
		print('NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[2]/(green_2013[2]+yellow_2013[2])*100)) + '%', ' NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[2]/(green_2017[2]+yellow_2017[2])*100)) + '%')
	elif letter == 'mp':
		print('MS and PhD:')
		print('ABC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[0]/(green_2013[0]+yellow_2013[0])*100)) + '%', ' ABC 2017 - Green Reporting: ' + str("{0:.0f}".format(green_2017[0]/(green_2017[0]+yellow_2017[0])*100)) + '%')
		print('FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[1]/(green_2013[1]+yellow_2013[1])*100)) + '%', ' FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[1]/(green_2017[1]+yellow_2017[1])*100)) + '%')
		print('NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[2]/(green_2013[2]+yellow_2013[2])*100)) + '%', ' NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[2]/(green_2017[2]+yellow_2017[2])*100)) + '%')
	else:
		print('Total:')
		print('ABC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[0]/(green_2013[0]+yellow_2013[0])*100)) + '%', ' ABC 2017 - Green Reporting: ' + str("{0:.0f}".format(green_2017[0]/(green_2017[0]+yellow_2017[0])*100)) + '%')
		print('FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[1]/(green_2013[1]+yellow_2013[1])*100)) + '%', ' FOX 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[1]/(green_2017[1]+yellow_2017[1])*100)) + '%')
		print('NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2013[2]/(green_2013[2]+yellow_2013[2])*100)) + '%', ' NBC 2013 - Green Reporting: ' + str("{0:.0f}".format(green_2017[2]/(green_2017[2]+yellow_2017[2])*100)) + '%')

    """Uncomment the following line to write sorted data to csv files."""
	#write_to_csv(channel_date,letter) 

"""This function writes data for each channel and date point into files sorted by event.
IMPORTANT: Make sure to delete the files from data/ that start with ABC, FOX or NBC. Otherwise new 
data will be simply be appended to the new file instead of overwritten"""
def write_to_csv(channel_date,letter):
	dates_to_topic = {
	'2013_04_15':'Boston_Marathon_Bombing',
	'2013_04_16':'Boston_Marathon_Bombing',
	'2013_04_17':'Boston_Marathon_Bombing', 
	'2013_04_18':'Boston_Marathon_Bombing', 
	'2013_04_19':'Boston_Marathon_Bombing',
	'2013_04_20':'Boston_Marathon_Bombing',
	'2013_04_21':'Boston_Marathon_Bombing', 
	'2013_05_19':'Midwest_Tornados', 
	'2013_05_20':'Midwest_Tornados',
	'2013_05_21':'Midwest_Tornados',
	'2013_05_22':'Midwest_Tornados',
	'2013_05_23':'Midwest_Tornados',  
	'2013_05_24':'Midwest_Tornados',
	'2013_05_25':'Midwest_Tornados',
	'2013_06_09':'NSA_File_Leak', 
	'2013_06_10':'NSA_File_Leak',
	'2013_06_11':'NSA_File_Leak',
	'2013_06_12':'NSA_File_Leak',
	'2013_06_13':'NSA_File_Leak',  
	'2013_06_14':'NSA_File_Leak',
	'2013_08_22':'Ghouta(Syria)_Chemical_Weapon_Attack', 
	'2013_08_23':'Ghouta(Syria)_Chemical_Weapon_Attack',
	'2013_08_24':'Ghouta(Syria)_Chemical_Weapon_Attack',
	'2013_08_25':'Ghouta(Syria)_Chemical_Weapon_Attack',
	'2013_08_26':'Ghouta(Syria)_Chemical_Weapon_Attack',  
	'2013_08_27':'Ghouta(Syria)_Chemical_Weapon_Attack',
	'2013_08_28':'Ghouta(Syria)_Chemical_Weapon_Attack',
	'2017_04_04':'Khan_Shaykhun(Syria)_Chemical_Weapon_Attack',
	'2017_04_05':'Khan_Shaykhun(Syria)_Chemical_Weapon_Attack',
	'2017_04_06':'Khan_Shaykhun(Syria)_Chemical_Weapon_Attack',
	'2017_04_07':'Khan_Shaykhun(Syria)_Chemical_Weapon_Attack',
	'2017_04_08':'Khan_Shaykhun(Syria)_Chemical_Weapon_Attack',
	'2017_04_09':'Khan_Shaykhun(Syria)_Chemical_Weapon_Attack',
	'2017_04_10':'Khan_Shaykhun(Syria)_Chemical_Weapon_Attack',
	'2017_05_12':'Ransomware_Cyber_Attack',
	'2017_05_13':'Ransomware_Cyber_Attack',
	'2017_05_14':'Ransomware_Cyber_Attack',
	'2017_05_15':'Ransomware_Cyber_Attack',
	'2017_05_16':'Ransomware_Cyber_Attack',
	'2017_05_17':'Ransomware_Cyber_Attack',
	'2017_09_20':'Hurricane_Maria',
	'2017_09_21':'Hurricane_Maria',
	'2017_09_22':'Hurricane_Maria',
	'2017_09_23':'Hurricane_Maria',
	'2017_09_24':'Hurricane_Maria',
	'2017_09_25':'Hurricane_Maria',
	'2017_09_26':'Hurricane_Maria',
	'2017_10_02':'Las_Vegas_Mass_Shooting',
	'2017_10_03':'Las_Vegas_Mass_Shooting',
	'2017_10_04':'Las_Vegas_Mass_Shooting',
	'2017_10_05':'Las_Vegas_Mass_Shooting',
	'2017_10_06':'Las_Vegas_Mass_Shooting',
	'2017_10_07':'Las_Vegas_Mass_Shooting'
	}
	show_length = {
	'ABC':30.0,
	'FOX':60.0,
	'NBC':30.0
	}

	"""The percentage of time an event was covered on a particular date and channel"""
	transcript_breakdown = []
	with open('reporting_percentage.csv', 'r') as f:
		transcript_breakdown = f.readlines()
	transcript_breakdown = [x.strip() for x in transcript_breakdown]  
	reporting_percentage = dict()
	for r in transcript_breakdown:
		item = r.split(', ')
		reporting_percentage[item[0]] = item[1]

	"""For each date/channel file, calculate the number of minutes the event is covered for.
	Then print the number of 'green reporting' minutes, 'yellow reporting' minutes, total coverage time and the date of the event
	This line is then written in the file for the channel and date the data was calculated for """
	for point in channel_date.keys():
		split_name = point.split('_')
		date = split_name[1]+'_'+split_name[2]+'_'+split_name[3]
		data_file = '../data/' + split_name[0] + '_' + dates_to_topic[date] + '.csv'
		report_percentage = reporting_percentage[split_name[0] + '_' + date]
		minutes = float(show_length[split_name[0]]) * float(report_percentage)

		with open(data_file, "a") as f:
			writer = csv.writer(f)
			if os.path.getsize(data_file) == 0:
				f.write('Green,Yellow,Minutes of Coverage,x')
				f.write('\n')
			total = channel_date[point][0] + channel_date[point][1]
			green_percent = (channel_date[point][0]/total) * minutes
			yellow_percent = (channel_date[point][1]/total) * minutes
			
			f.write(str('{0:.1f}'.format(green_percent)) + ',' + str('{0:.1f}'.format(yellow_percent)) + ',' + str('{0:.1f}'.format(minutes)) + ',' + str(split_name[1]) +'-'+ str(split_name[2]) +'-'+ str(split_name[3]))
			f.write('\n')
	print('Done writing data to file')

"""This function performs simple metrics on the workers that took the surveys and prints them"""
def workers(worker_ids): 
	worker_ids.sort()
	only_ids = [] 
	count_workers = dict()
	"""Determine the number of surveys each Worker completed"""
	for w in worker_ids: 
		only_ids.append(w[0])
		if w[0] in count_workers.keys():
			count = count_workers[w[0]]
			count += 1
			count_workers[w[0]] = count 
		else: 
			count_workers[w[0]] = 1
	"""Calculate the number of people who answered more than two surveys and store the surveys they completed"""
	multiple = 0
	for key in count_workers.keys():
		if(count_workers[key] > 2):  
			multiple += 1
			repeated_tests = [i[1] for i in worker_ids if i[0]==key]


	print(multiple) #Number of people who completed more than 2 surveys
	print(len(only_ids)) #Total number of IDs
	print(len(set(only_ids))) #Number of unique IDs

if __name__ == '__main__':

	#Read in data from raw data file
    infile_one = '../data/raw_data.csv'
    fname = open( infile_one, "r")
    reader = csv.reader(fname)

    worker_ids = [] 
    people_data = []
    tested_file_names = []

	# Dictionaries for each demographic we want to test. Additional dictionary for looking at all data
    responses_d = dict()
    responses_r = dict()
    responses_o = dict()
    responses_HS = dict()
    responses_AS_BS = dict()
    responses_MS_PhD = dict()
    responses = dict()


    #For each file, read in the data and sort them into their appropriate dictionaries
    for line in reader:
    	tested_file = line[0]
    	data = line[1]
    	strs = data.replace('[','').split('],')
    	worker_data = list(map(list, ((s.replace(']','').split(',')) for s in strs)))
    	date = tested_file.split("/")[-1]
    	ans = []
    	for r in worker_data:
    		worker_id = r[0].strip()
    		worker_ids.append((worker_id,tested_file))
    		demo = []
    		try:
	    		for i in range(1,8):
	    			demo.append(r[i].strip())
	    		people_data.append((worker_id,demo))
	    	except:
	    		print(r)
    		if date in responses.keys():
    			data = responses[date]
    			temp = []
    			for i in range(8,len(r)):
    				temp.append(r[i].strip())
    			data.append(temp)
    			responses[date] = data
    		else:
    			data = []
    			for i in range(8,len(r)):
    				data.append(r[i].strip())
    			responses[date] = [data]

    		"""To save data for certain demographics, create an additional dictionary above and add any responses that contain that demographic to the dictionary. You can separately call the calculation function for each demographic to be tested."""
    		#Political data demographics
    		if "'republican'" in demo:
    			if date in responses_r.keys():
	    			data = responses_r[date]
	    			temp = []
	    			for i in range(8,len(r)):
	    				temp.append(r[i].strip())
	    			data.append(temp)
	    			responses_r[date] = data
	    		else:
	    			data = []
	    			for i in range(8,len(r)):
	    				data.append(r[i].strip())
	    			responses_r[date] = [data]
	    	elif "'Democratic'" in demo:
	    		if date in responses_d.keys():
	    			data = responses_d[date]
	    			temp = []
	    			for i in range(8,len(r)):
	    				temp.append(r[i].strip())
	    			data.append(temp)
	    			responses_d[date] = data
	    		else:
	    			data = []
	    			for i in range(8,len(r)):
	    				data.append(r[i].strip())
	    			responses_d[date] = [data]
	    	else:
	    		if date in responses_o.keys():
	    			data = responses_o[date]
	    			temp = []
	    			for i in range(8,len(r)):
	    				temp.append(r[i].strip())
	    			data.append(temp)
	    			responses_o[date] = data
	    		else:
	    			data = []
	    			for i in range(8,len(r)):
	    				data.append(r[i].strip())
	    			responses_o[date] = [data]

	    	#Education demographics
	    	if "'High School Diploma or Equivalent'" in demo:
	    		if date in responses_HS.keys():
	    			data = responses_HS[date]
	    			temp = []
	    			for i in range(8,len(r)):
	    				temp.append(r[i].strip())
	    			data.append(temp)
	    			responses_HS[date] = data
	    		else:
	    			data = []
	    			for i in range(8,len(r)):
	    				data.append(r[i].strip())
	    			responses_HS[date] = [data]
	    	elif ("'Associate'" or "'Bachelor'") in demo:
	    		if date in responses_AS_BS.keys():
	    			data = responses_AS_BS[date]
	    			temp = []
	    			for i in range(8,len(r)):
	    				temp.append(r[i].strip())
	    			data.append(temp)
	    			responses_AS_BS[date] = data
	    		else:
	    			data = []
	    			for i in range(8,len(r)):
	    				data.append(r[i].strip())
	    			responses_AS_BS[date] = [data]
	    	elif ("'Master'" or "'Doctoral Degree'") in demo:
	    		if date in responses_MS_PhD.keys():
	    			data = responses_MS_PhD[date]
	    			temp = []
	    			for i in range(8,len(r)):
	    				temp.append(r[i].strip())
	    			data.append(temp)
	    			responses_MS_PhD[date] = data
	    		else:
	    			data = []
	    			for i in range(8,len(r)):
	    				data.append(r[i].strip())
	    			responses_MS_PhD[date] = [data]

    """Comment out the demographics you do not want to calculate """
    sort_calculate(responses, None) 
    # sort_calculate(responses_d, 'd')
    # sort_calculate(responses_r, 'r')
    # sort_calculate(responses_o, 'o')
	# sort_calculate(responses_HS, 'h')
	# sort_calculate(responses_AS_BS, 'ab')
	# sort_calculate(responses_MS_PhD, 'mp')
	# demographics(people_data)
	# workers(worker_ids) 