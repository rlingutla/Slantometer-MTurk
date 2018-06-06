aws_access_key=''
aws_secret_key=''
PROD = False

if PROD:
	host='mechanicalturk.amazonaws.com' 
	form='https://mturk.com/mturk/externalSubmit' 
	result="https://mturk.com/mturk/preview?groupId={}"
else:
	host='mechanicalturk.sandbox.amazonaws.com'
	form='https://workersandbox.mturk.com/mturk/externalSubmit'
	result="https://workersandbox.mturk.com/mturk/preview?groupId={}"