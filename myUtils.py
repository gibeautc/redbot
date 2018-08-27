#!/usr/bin/env python3



import string

table = str.maketrans({key: None for key in string.punctuation})

def stripWord(word):
	'''
	returns the word after processing it, it stips white space, removes punctuation, and converts to lower case
	'''
	word=word.strip()
	word=word.lower()
	word = word.translate(table) 
	return word













if __name__=="__main__":
	words=['Hello',"GoodBye","[yep]","s ome spaces   ",""," ","it's"]
	print(words)
	new=[]
	for w in words:
		new.append(stripWord(w))
	
	print(new)
	
	for p in string.punctuation:
		print(p)
