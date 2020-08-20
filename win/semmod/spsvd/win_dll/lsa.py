#!/usr/bin/python
import bsddb
import string
import cPickle
import numpy 
import extractCorpus
from math import *

class createSpace:
	def __init__(self, DatabaseName, filename, dimensions=2, iterations=1200):
		eC = extractCorpus.ExtractCorpus()
		eC.get_matrices(DatabaseName, filename, dimensions, iterations)

class lsaSpace:
	def __init__(self, DatabaseName = "./tasaDB"):
		self.db = bsddb.btopen(DatabaseName)

	def getSingularValues(self):
		return(cPickle.loads(self.db["SingularValues"]))

	def getTermVector(self, term):
		weight, vector = cPickle.loads(self.db[term])
		return(vector)

	def getTermWeightAndVector(self, term):
		return(cPickle.loads(self.db[term]))

	def length(self, vector):
		return(sqrt(numpy.dot(vector, vector)))
	
	def cosine(self, vector1, vector2):
		try:
			return(numpy.dot(vector1, vector2)/self.length(vector1)/self.length(vector2))
		except:
			return(0.0)

	def cosTermDoc(self, term, doc):
		sqrtSVs = numpy.sqrt(self.getSingularValues())
		try:
			termVec = self.getTermVector(term) * sqrtSVs
			docVec = self.getWeightedTerms(doc) * sqrtSVs
			return(self.cosine(termVec, docVec))
		except:
			print "Hi"
			return(None)

	def cosTermTerm(self, term1, term2):
		SVs = self.getSingularValues()
		try:
			term1Vec = self.getTermVector(term1) * SVs
			term2Vec = self.getTermVector(term2) * SVs
			return(self.cosine(term1Vec, term2Vec))
		except:
			return(None)

	def cosDocDoc(self, doc1, doc2):
		SVs = self.getSingularValues()
		try:
			doc1Vec = self.getWeightedTerms(doc1) * SVs
			doc2Vec = self.getWeightedTerms(doc2) * SVs
			return(self.cosine(doc1Vec, doc2Vec))
		except:
			return(None)

	def getDocVector(self, doc):
 		SVs = self.getSingularValues()
		return(self.getWeightedTerms(doc) * SVs)

	def size(self, ):
		return(len(self.db)-1)

	def numberOfFactors(self):
		return(len(self.getSingularValues()))

	def __str__(self):
		return("Number of Terms = " + str(self.size()) + " Number of Factors = " + str(self.numberOfFactors()))

	def getWeightedTerms(self, words):
		# split words and sort
		words = string.split(words.lower())
		counts = {}
		for word in words:
			if counts.has_key(word):
				counts[word] += 1
			else:
				counts[word] = 1
		result = numpy.zeros(self.numberOfFactors())
		for word in counts.keys():
			try:
				weight, vector = self.getTermWeightAndVector(word)
				result += vector * weight * log(counts[word]+1)
			except:
				pass
			
		return(result)


	def getTimeDate(self):
		return self.db['SpaceCreationTime']

		
	
if __name__ == "__main__":
	space = lsaSpace()
	print space
	print "Size of database = ", space.size()
	singularValues = space.getSingularValues()
	dog = space.getTermVector("dog") * singularValues
	cat = space.getTermVector("cat") * singularValues
	leash = space.getTermVector("leash") * singularValues
	print "cosine(dog, cat) = " , space.cosine(dog, cat)
	print "cosine(dog, leash) = ", space.cosine(dog, leash)
	vec = space.getWeightedTerms("hello there hello ")
	print vec[0:10]
	print space.cosTermDoc("hello", "hello there here is some text")
	print space.cosTermDoc("dog", "hello there here is some text")
	print space.cosTermDoc("dog", "puppy cat leash walk .")

