"""This script is used to break a large file with lots of sentences into smaller files of 
at most 20 sentences. Order of sentences are randomized as well
@Param: name of text filen
@Output: file with 20 sentences from original file """
import os.path 
import sys
from random import shuffle

print(os.path.splitext(sys.argv[1]))
filename = os.path.splitext(sys.argv[1])[0] 
print(filename)

with open(sys.argv[1]) as f:  
	count = 0
	control = f.read().split('\n\n') 
	shuffle(control)
	for i in range(0,len(control),20):
		count += 1
		outfile1 = '../Chunked_files/' + filename + '_' + str(count) +'.txt'
		with open(outfile1, "w") as f:
			f.write('\n\n'.join(control[i:i+20]))