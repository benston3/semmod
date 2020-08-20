#!/usr/bin/python2.5
import math
import scipy.sparse as SP
import numpy.ctypeslib as cl
from numpy import *
import numpy.random as R
import ctypes as c


NumberOfWords = 10
NumberOfDocs = 9
ALPHA = 0.3
BETA = 0.1
NumberOfTopics = 2

m = SP.csc_matrix((NumberOfWords, NumberOfDocs))
m[0,5] = 0.474
m[0,7] = 0.474
m[1,2] = 0.474
m[1,4] = 0.474
m[2,1] = 0.474
m[2,5] = 0.474
m[3,7] = 0.474
m[3,8] = 0.474
m[4,1] = 0.474
m[4,2] = 0.474
m[5,6] = 0.474
m[5,8] = 0.474
m[6,0] = 0.347
m[6,3] = 0.347
m[6,4] = 0.347
m[7,7] = 0.474
m[7,8] = 0.474
m[8,0] = 0.474
m[8,3] = 0.474
m[9,0] = 0.256
m[9,1] = 0.256
m[9,5] = 0.256
m[9,6] = 0.256


topicslibrary = cl.load_library("topics",".")  

#double topics( long nnz, long NumberOfDocs, long NumberOfWords, long *docPtr, long *wordID, double *values, long *wordByTopic, long *topicCount, long *docByTopic, long NumberOfTopics, double ALPHA, double BETA, long *topics);

topicslibrary.topics.argtypes = [cl.c_intp, # nnz \
                       cl.c_intp, # NumberOfDocs \
                       cl.c_intp, # NumberOfWords \
                       cl.ndpointer(int32, flags='aligned, contiguous'), # docPtr \
                       cl.ndpointer(int32, flags='aligned, contiguous'), # wordID \
                       cl.ndpointer(float64, flags='aligned, contiguous'), # values \
                       cl.ndpointer(int32, flags='aligned, contiguous'), # wordByTopic \
                       cl.ndpointer(int32, flags='aligned, contiguous'), # topicCount \
                       cl.ndpointer(int32, flags='aligned, contiguous'), # docByTopic \
                       cl.ndpointer(int32, flags='aligned, contiguous'), # topics \
                       cl.c_intp, # NumberOfTopics \
                       c.c_float, # ALPHA \
                       c.c_float # BETA \
                       ]


wordByTopic = zeros((NumberOfWords, NumberOfTopics), int)
docByTopic = zeros((NumberOfDocs, NumberOfTopics), int)
topics = R.randint(0, NumberOfTopics, m.getnnz())
topicCount = zeros(NumberOfTopics, int)

# Initialize Matrices
doc = 0
for i in xrange(m.getnnz()):
  while m.indptr[doc+1] <= i:
    doc += 1
  print i, m.rowind[i], doc, topics[i]
  topicCount[topics[i]] += 1
  wordByTopic[m.rowind[i], topics[i]] += 1
  docByTopic[doc, topics[i]] += 1

print "wordByTopic"
print wordByTopic
print "docByTopic"
print docByTopic
print "topics"
print topics
print "topicCount"
print topicCount

for i in xrange(10):
  ans = topicslibrary.topics( int(m.getnnz()), NumberOfDocs, NumberOfWords, m.indptr, m.rowind, m.data, wordByTopic, topicCount, docByTopic, topics, NumberOfTopics, ALPHA, BETA)


print "wordByTopic"
print wordByTopic
print "docByTopic"
print docByTopic
print "topics"
print topics
print "topicCount"
print topicCount
      

  
