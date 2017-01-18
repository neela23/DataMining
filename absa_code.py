#import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import csv
import nltk
from nltk.corpus import sentiwordnet as swn


result=[]
food_list=['food']
service_list=['service']
place_list=['place']
price_list=['price']
others_list=[]
def add_to_list(word):
	global food_list, service_list, place_list, price_list, other_list
	l0=[]
	l1=[]
	l2=[]
	l3=[]
	for food in food_list:
		l0.append(returnSimilarity(word,food))
	for service in service_list:
		l1.append(returnSimilarity(word,service))
	for place in place_list:
		l2.append(returnSimilarity(word,place))
	for price in price_list:
		l3.append(returnSimilarity(word,price))
	max0=max(l0)
	max1=max(l1)
	max2=max(l2)
	max3=max(l3)
	l=[max0,max1,max2,max3]
	if max(l)> 0.1:
		list_num=l.index(max(l))
		if list_num is 0:
			food_list.append(word)
		if list_num is 1:
			service_list.append(word)
		if list_num is 2:
			place_list.append(word)
		if list_num is 3:
			price_list.append(word)
	else:
		others_list.append(word)

def returnAdjNounRelation(taggedText, word, index):
	arr = []
	for i in range(index-1, index-6, -1):
		w, p = taggedText[i]
		if w in ['.', '!']:
			break
		if p in ['NN', 'NNP', 'N']:
			arr.append(w)
	
	for i in range(index+1, index+6):
                w, p = taggedText[i]
                if w in ['.', '!']:
                        break
                if p in ['NN', 'NNP', 'N']:
                        arr.append(w)
	return arr
	
	
	#rd_parser = nltk.RecursiveDescentParser(grammar1)
	#for tree in rd_parser.parse(taggedText):
	 #     print(tree)
	#wordInText = '\''+word+'\'' + ', \'JJ\''
	#print wordInText
	#index = taggedText.index(word, wordInText)
	#print index


def returnSimilarity(word1, word2):
	w1 = wn.synsets(word1, pos = wn.NOUN) #wn.synsets('dog', pos=wn.VERB) if we are doing POS
	w2 = wn.synsets(word2)
	
	if len(w1) is 0:
		return 0
	
	a = w1[0]
	b = w2[0]

	return a.lin_similarity(b, semcor_ic)

def returnPositivityScore(word):
	w1 = swn.senti_synsets(word, 'a')
	#w1 = wn.synsets(word, pos = wn.ADJ)
	if len(w1) is 0:
		return 0
	#happy0 = list(happy)[0
	pos_score = w1[0].pos_score()
	neg_score = w1[0].neg_score()
	obj_score = w1[0].obj_score()
	print word, pos_score,neg_score, obj_score
	if word in positiveList:
		return pos_score if pos_score>0 else 0.125
	if word in negativeList:
                return neg_score*-1 if neg_score>0 else -0.125
	#if pos_score< neg_score:
	#	return neg_score
	if obj_score > pos_score and obj_score > neg_score:
		return 0
	return (pos_score - neg_score)


def returnAvg(score, count):
	if count is 0:
		return score
	return score/count
def determineCategoryScores(adjDict, adjScore, stars, index, writer):
	
	foodScore = 0
	foodCount = 0
	serviceScore = 0
	serviceCount = 0
	placeScore = 0
	placeCount = 0
	priceScore = 0
	priceCount = 0
	otherScore = 0
	otherCount = 0
	for adj, nouns in adjDict.items():
		score = adjScore[adj]
		for noun in nouns:
			if noun in food_list:
				foodScore = foodScore + score
				foodCount = foodCount + 1
			elif noun in service_list:
				serviceScore = serviceScore + score
				serviceCount = serviceCount + 1
			elif noun in place_list:
				placeScore = placeScore + score
				placeCount = placeCount + 1 
			elif noun in price_list:
				priceScore = priceScore + score
				priceCount = priceCount + 1
			elif noun in others_list:
				otherScore = otherScore + score
				otherCount = otherCount +1

		writer.writerow({'reviewnum':str(index), 'food':str(returnAvg(foodScore , foodCount)),'service':str(returnAvg(serviceScore , serviceCount)),'place':str(returnAvg(placeScore , placeCount)),'price':str(returnAvg(priceScore , priceCount)),'others':str(returnAvg(otherScore , otherCount)), 'stars':str(stars)})

	

def processData():
	c = 0
	with open('reviews.csv') as csvfile:
	     reader = csv.DictReader(csvfile)
	     with open('scores.csv', 'w') as csvfile:
                fieldnames = ['reviewnum', 'food', 'service' , 'place' , 'price' , 'others', 'stars']
                writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	        writer.writeheader()	
		for row in reader:
	     	    	text = row["text"]
			stars = row["stars"]
			text = text.lower()
			text = nltk.word_tokenize(text)
			t = nltk.Text(text)
			c = c+1
			adjDict = dict()
			adjScore = dict()
			if c > 10000:
				break
			try:
				taggedText = nltk.pos_tag(t)
			except ValueError:
				continue
			print taggedText
			index = 0
			for word, pos in taggedText: # remove the call to nltk.pos_tag if `sentence` is a list of tuples as described above						        
				
				if pos in ['NN', "NNP"]: # feel free to add any other noun tags
            				add_to_list(word)
				
				if pos in ['JJ']:
					# Look for nouns in the nearby area
					score = returnPositivityScore(word)
					if score is not 0:
						if index>0:
							prevWord, prevPos = taggedText[index-1]
							if prevWord in ['no', 'not', 'nothing']:
								score = score * -1
						
						adjScore[word] = score*5
						arrNouns = returnAdjNounRelation(taggedText, word, index)
						if word in adjDict:
							adjDict[word].extend(arrNouns)
						else:
							adjDict[word] = arrNouns
						#print word
				index = index + 1
			determineCategoryScores(adjDict, adjScore, stars, c, writer)
			# Write to scv
semcor_ic = wordnet_ic.ic('ic-semcor.dat')

fPos = open('positive-words.txt', 'r')
fNeg = open('negative-words.txt', 'r')

positiveList = fPos.read()
negativeList = fNeg.read()

fPos.close()
fNeg.close()

#fieldnames = ['reviewnum', 'food', 'service' , 'place' , 'price' , 'others']

#writer = csv.DictWriter('test', fieldnames = fieldnames)


processData()
