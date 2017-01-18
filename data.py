import json
import csv

file_directory = "yelp_academic_dataset_review.json"
json_data=open(file_directory).read()
#print json_data
#print json_data


arr = [] # Array of dictionaries
i=0
with open("yelp_academic_dataset_review.json") as f:
    	for line in f:
		k = json.loads(line)
	#	print k["stars"]
	#	print k["text"]
		votes = k["votes"]
		if votes["useful"]>1 and votes["funny"]<1:
			review = dict()
			review["stars"] = k["stars"]
			review["text"] = k["text"]
			arr.append(review)

with open('reviews.csv', 'w') as csvfile:
    fieldnames = ['stars', 'text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for line in arr:
	text = line['text'].encode("utf8")
	writer.writerow({'stars':line['stars'], 'text':text})
		
	#users = [json.loads(line) for line in f]
    	#print users
#    i=i+1
 #   if i>20:
#	break
'''

count = 0
for a in json_data:
	count = count+1
	if count<10:
		print a
print count
'''
