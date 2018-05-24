"""srt_parse.py converts srt files into a more readable format
@Param: The name of a .srt file 
@Return: Text file with the text in the .srt file converted in human-readable sentences. 
        Time-stamps and most advertisements have been removed from transcript"""


import sys 
import re
from itertools import groupby
from ast import literal_eval
import os
import nltk.data
nltk.download('punkt')

"""Run the following command in Terminal to run the script on multiple srt files. 
Run in direcrtory of .srt files."""
#for f in *; do python <location of srt_parse.py> $f; done

infile = sys.argv[1]
final = ''
file_name = '' 
file_extension = os.path.splitext(infile)[1] 
if(file_extension == '.srt'): 
    k=infile.split('_')
    if("ABC" in infile): 
        date = k[1][:4] + '_' + k[1][4:6] + '_' + k[1][6:]
        file_name = 'ABC_' + date + '.txt'
    elif("FOX" in infile):
        date = k[1][:4] + '_' + k[1][4:6] + '_' + k[1][6:]
        file_name = 'FOX_' + date + '.txt'
    else:
        date = k[1][:4] + '_' + k[1][4:6] + '_' + k[1][6:]
        file_name = 'NBC_' + date + '.txt' 
     

    with open(infile) as f:
        res = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b] 
        for r in res: 
        	r = r[2:]
        	r_sub = [re.sub('[>>]', '', x) for x in r] 
        	r_minus_name = [x.split(':', 1) for x in r_sub] 
        	flat_list = [item for sublist in r_minus_name for item in sublist] 
        	#print(flat_list)
        	lowercase_letters = [c for c in flat_list for b in c if b.islower()] 

        	if(len(lowercase_letters) == 0):
        		for l in flat_list:
        			final += l
        		#print(final)
        	# else: 
        	# 	print(r_sub)

    f_out = open('../Cleaned_Files/' + file_name,'w')

    #print(final)

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    final = final.strip()
    sentence = '\n\n'.join(tokenizer.tokenize(final.decode('utf8')))   
    sentences = sentence.splitlines()
    final_sentence = '' 

    f_out.write(sentence.encode('utf8'))

    f_out.close()
