#!/usr/bin/python
#import Numeric as NM
#import spsvd as C2C
import cPickle
import bsddb
from sys import *
import math
import time

import numpy.ctypeslib as cl
import numpy as NY

class DimensionInputException(Exception):
  '''A user-defined exception class.'''
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class ExtractCorpus:
  def newDoc(self,line):
    ret = False
    if(line == "\n") or (line == "\r\n"):
      ret = True
  
    return ret

  def get_matrices(self, DatabaseName, filename, dimensions, iterations):

    #returns 1) Word ID Hash
    corpus_types_id = dict()
    #        2) Word frequency Hash
    corpus_types_freq = dict()
    #        3) Number of Non-zeros Hash - NNZ
    NNZ = 0
    id_count = 0   # counter for word ids
    #        4) Number of documents
    doc_count = 0  #count number of documents


    #open corpus file
    f = open(filename, "r")
    
    #extract types from document corpus
    line_holder = ""
    for line in f:
      run_split = False
      #check for new documents  
      if self.newDoc(line):
        doc_count += 1
        run_split = True
      #check to see if this is the first document
      #if first document run_split is already defined True
      #elif doc_count == 0:
        #doc_count += 1

      if not (run_split):
        if(len(line_holder) > 0):
          line_holder = "%s %s" % (line_holder, line[:-1])
        else:
          line_holder = line

      #split the tokenised lines
      if(run_split):
        NNZ_dict = dict()
        for words in line_holder.split(" "):
          word = words.replace("\n", "")
          
          #insert into type dictionary
          #check if word is already in dict_types
          if(word in corpus_types_id): 
            corpus_types_freq[corpus_types_id[word]] += 1
          else:
            corpus_types_id[word] = id_count
            corpus_types_freq[corpus_types_id[word]] = 1
            id_count += 1

          if(word in NNZ_dict):
            z = 0
          else:
            NNZ_dict[word] = 1
            NNZ += 1

        del NNZ_dict
        line_holder = ""

    ######
    # check doc number is >= dimensions
    try:
      if dimensions > doc_count:
        raise DimensionInputException(dimensions)
      
    except DimensionInputException, e:
        msg = '\nDimensionInputException:\nThe number of dimensions (%d),\nneeds to be less than or equal to\nthe number of corpus documents (%d)\n' % (e.value, doc_count) 
        exit(msg)  

    ######
    ##second pass to get:
    ## 1) Numeric array of type frequencies per doc
    ## 2) Numeric array of associated word ids
    ## 3) doc pointer array
    ## 4) Weighted type array

    types_mtx = NY.zeros(NNZ)
    types_mtx_counter = 0
    types_id_mtx = NY.zeros(NNZ, NY.int)
    types_entropy_mtx = NY.zeros(id_count)


    doc_pointer = NY.zeros((doc_count + 1), NY.int)
   
    doc_pointer_position = 0
    doc_pointer_count = 0
    f.close()
    del f

    #open corpus file
    
    f = open(filename, "r")
    line_holder = ""

    for line in f:
      run_split = False
      #check for new documents  
      if self.newDoc(line):
        doc_pointer[doc_pointer_position] = doc_pointer_count
        doc_pointer_position += 1
        run_split = True
      #check to see if this is the first document
      #if first document run_split is already defined True
      #elif doc_pointer_position == 0:
        #doc_pointer[doc_pointer_position] = doc_pointer_count
        #doc_pointer_position += 1

      if not (run_split):
        if(len(line_holder) > 0):
          line_holder = "%s %s" % (line_holder, line[:-1])
        else:
          line_holder = line

      #split the tokenised lines
      if(run_split):
        #print "Line holder: %s" % line_holder
        #print line_holder.split(" ")
        doc_types_freq = dict()
        doc_types_id = dict()
        doc_types_id_sort = []
        for words in line_holder.split(" "):
          word = words.replace("\n", "")
          #print "word: %s" % word
          #insert into type this docs dictionary
          #check if word is already in doc_types_freq
          if(word in doc_types_freq): 
            doc_types_freq[word] += 1
          else:         
            word_id = corpus_types_id[word]
            doc_types_freq[word] = 1
            doc_types_id[word_id] = word
            doc_types_id_sort.append(word_id)
            doc_pointer_count += 1

        #re-order type ids
        doc_types_id_sort.sort()

        global_i = 1

        for ids in doc_types_id_sort:
        #calculate sum tf log2 tf for weighting matrix
          tf = doc_types_freq[doc_types_id[ids]]
          types_entropy_mtx[ids] += tf * (math.log(tf,2))

        #enter type frequencies into matrix
          types_mtx[types_mtx_counter] = doc_types_freq[doc_types_id[ids]]
          types_id_mtx[types_mtx_counter] = ids
          types_mtx_counter += 1

        del doc_types_id_sort, doc_types_freq, doc_types_id
        line_holder = ''

    #calculate weight type by document matrix
    for k in range(NNZ):      
      gf = corpus_types_freq[int(types_id_mtx[k])]
      n1 = gf * (math.log(gf,2))      
      n2 = types_entropy_mtx[int(types_id_mtx[k])]
      d = float(gf * math.log(doc_count,2))
      #calculate entropy
      entropy = 1 - ((n1-n2)/d)
      local_ij = math.log(types_mtx[k] + 1)
      aij = local_ij * entropy

      types_mtx[k] = aij 
  

 
    #send to c program
    doc_pointer[doc_count] = NNZ
    Ut_value = NY.zeros(id_count * dimensions)
    singular_values = NY.zeros(dimensions)
    Vt_value = NY.zeros(dimensions * doc_count)

    spsvd_dll = cl.load_library("spsvd.dll",".")  
    vS = spsvd_dll.get_vectorSpace
    # extern "C" __declspec(dllexport) double get_vectorSpace( long dimensions, long iterations, long n_types, long n_docs, long nnz, long *docPtr, long *wordID, double *weightings, double *ut , double *sing, double *vt  );

    vS.argtypes = [cl.c_intp,cl.c_intp,cl.c_intp,cl.c_intp,cl.c_intp, cl.ndpointer(cl.c_intp, flags='aligned, contiguous'), cl.ndpointer(cl.c_intp, flags='aligned, contiguous') , cl.ndpointer(float, flags='aligned, contiguous'), cl.ndpointer(float, flags='aligned, contiguous'), cl.ndpointer(float, flags='aligned, contiguous'), cl.ndpointer(float, flags='aligned, contiguous') ]

    ans = vS( int(dimensions), int(iterations), int(id_count), int(doc_count), int(NNZ), doc_pointer,  types_id_mtx, types_mtx, Ut_value, singular_values, Vt_value );


    #enter values in DatabaseName
    db = bsddb.btopen(DatabaseName)
    
    db['SpaceCreationTime'] = time.asctime()


    #SingularValues
    SVs = NY.zeros(dimensions)
    for i in xrange(dimensions):
      SVs[i] = singular_values[i]

    

    db['SingularValues'] = cPickle.dumps(SVs)

    #Put Ut values and global weightings into DatabaseName 
    for words in corpus_types_id:
      Uts = NY.zeros(dimensions)
      for j in xrange(dimensions):
        Uts[j] = Ut_value[((j*id_count)+corpus_types_id[words])]

      gf = corpus_types_freq[corpus_types_id[words]]
      n1 = gf * (math.log(gf,2))
      n2 = types_entropy_mtx[corpus_types_id[words]]
      d = float(gf * math.log(doc_count,2))
      entropy = 1 - ((n1-n2)/d)     

      db[words] = cPickle.dumps([entropy,Uts])

    db.close()

    #print
    #print "Vt"
    #for i in xrange(dimensions * doc_count):
       # print Vt_value[i],
    #print

    f.close()

   



    
