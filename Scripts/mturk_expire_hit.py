"""This script is used to get rid of any hits that we want to delete. 
HIT will be set to expire immediately so no one else can complete it.
200 response code will be returned upon success; an error will be printed otherwise
  """

#import necessary libraries
import boto
import boto3
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import HTMLQuestion
client = boto3.client('mturk')
from variables import aws_access_key, aws_secret_key, host, form, result

# Connection to MTurk
mtc = MTurkConnection(aws_access_key_id=aws_access_key,
aws_secret_access_key=aws_secret_key,
host=host)

#Enter HIT IDs into the following list
ids=["329E6HTMSWXS62LHSRDAIKNNL3KK3C"]

for i in ids:
	try:
		response = client.update_expiration_for_hit(
					    HITId=i,
					    ExpireAt=0
					) 
		print(response)
	except BaseException as e:
		print(e)