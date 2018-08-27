#!/usr/bin/env python3

import time
import praw
from termcolor import colored
import pickle
import sys

from myUtils import *


ignoreWords=[]
#triggerWords=[]
interestWords=[]

def dumpData(data):
	print("AUTO SAVING DATA")
	pickle.dump(data,open('data.p','wb'))
	
def loadData():
	return pickle.load(open('data.p','rb'))

def loadTrigger():
	global triggerWords
	#get ignore words from file
	f=open("triggerWords")
	data=f.read()
	triggerWords=data.split("\n")
	f.close()

def loadInerest():
	global interestWords
	#get ignore words from file
	f=open("ignoreWords")
	data=f.read()
	interestWords=data.split("\n")
	f.close()


def loadIgnore():
	global ignoreWords
	#get ignore words from file
	f=open("ignoreWords")
	data=f.read()
	ignoreWords=data.split("\n")
	f.close()

def logTrigger(t):
	f=open("triggerLog","a+")
	f.write(t.title+"\n")
	f.write(t.selftext+"\n")
	try:
		f.write(t.url+"\n")
	except:
		pass
	f.write(t.id+"\n\n\n")
	f.close()
	
def logInterst(t):
	f=open("interestLog","a+")
	f.write(t.title+"\n")
	f.write(t.selftext+"\n")
	try:
		f.write(t.url+"\n")
	except:
		pass
	f.write(t.id+"\n\n\n")
	f.close()

class WordList():
	def __init__(self):
		self.words=[]
		self.totalPosts=0
	def addWord(self,word,sub):
		for tw in self.words:
			if tw.word==word:
				#we have a repeat word
				tw.count=tw.count+1
				tw.ids.append(sub.id)
				tw.mostRecent=sub
				tw.lastHeard=time.time()
				self.Sort()
				return
		#if we get here, we dont have the word in the list
		newWord=TrendWord(word)
		newWord.mostRecent=sub
		self.words.append(newWord)
		self.Sort()
	def printlist(self,num):
		#prints the top num used words
		for x in range(num):
			perc=float(self.words[x].count)/float(self.totalPosts)
			perc=str(perc*100)
			perc=perc[:4]
			if self.words[x].lastRank<0:
				print(self.words[x].word+": ",perc,self.words[x].mostRecent.url)
			elif self.words[x].lastRank<x:
				#red
				print(colored((self.words[x].word+": "+perc+"  "+self.words[x].mostRecent.url),'red'))
			elif self.words[x].lastRank>x:
				#green
				print(colored(self.words[x].word+": "+perc+"  "+self.words[x].mostRecent.url,'green'))
			else:
				print(self.words[x].word+": ",perc, self.words[x].mostRecent.url)
			self.words[x].lastRank=x
		print("\n\n")
		
	def Sort(self):
		#sort the list in place...
		self.words.sort(key=lambda x: x.count, reverse=True)
	def Scrub(self):
		for w in self.words:
			if w.word in ignoreWords:
				print("Removing due to change in ignore words: ",w.word)
				self.words.remove(w)
			if time.time()-w.lastHeard>60*60:
				print("Removing due to age: ",w.word)
				self.words.remove(w)

class TrendWord():
	def __init__(self,word):
		self.word=word
		self.firstHeard=time.time()
		self.lastHeard=time.time()
		self.count=1
		self.ids=[]
		self.lastRank=-1
		self.mostRecent=None

loadIgnore()
loadTrigger()
reddit=praw.Reddit('bot1')
subreddit=reddit.subreddit("all")


try:
	trendWords=loadData()
	print("Data Loaded")
except:
	print("Failed to load data")
	print(sys.exc_info())
	trendWords=WordList()

lastShow=time.time()
lastScrub=time.time()
for submission in subreddit.stream.submissions():
	trendWords.totalPosts+=1
	if time.time()-lastScrub>30:
		trendWords.Scrub()
		dumpData(trendWords)
		lastScrub=time.time()
	if time.time()-lastShow>5:
		loadIgnore()
		loadTrigger()
		loadInerest()
		trendWords.printlist(50)
		lastShow=time.time()
	titleWords=submission.title.split(" ")
	for w in titleWords:
		word=stripWord(w)
		if len(word)<3:
			continue
		if word not in ignoreWords:
			trendWords.addWord(word,submission)
		if word in triggerWords:
			print("Trigger Logged:",word,"|")
			logTrigger(submission)
