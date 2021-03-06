// topics.cpp : Defines the entry point for the DLL application.
//

#include "stdafx.h"
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include "cokus.h"

#define myrand()  (double) (((unsigned long) randomMT()) / 4294967296.)
#define TRUE 1
#define FALSE 0
#define DllExport __declspec( dllexport )


extern "C"
{
long **toLong2DArray(long *arr, int rows, int cols){
/* convert a long * to a 2D long array */

  long **carray;
  int i;

  carray = (long **) malloc(rows * sizeof(long *));
  if (!carray) {free(carray); return NULL;}

  carray[0] = arr;

  for (i = 1; i < rows; i++) carray[i] = carray[i-1] + cols;
  return(carray);
}


DllExport double topics( long nnz, long NumberOfDocs, long NumberOfWords, long *docPtr, long *wordID, double *values, long *wordByTopic, long *topicCount, long *docByTopic, long *topics, long NumberOfTopics, double ALPHA, double BETA)
{


  int i, j, temp, doc, v;
  double totalprob, WBETA, r, max;
  double *probs;
  long **wordByTopicArray, **docByTopicArray, topic, wordInstance;

  wordByTopicArray = toLong2DArray(wordByTopic, NumberOfWords, NumberOfTopics);
  docByTopicArray = toLong2DArray(docByTopic, NumberOfDocs, NumberOfTopics);

  if (FALSE){
    // print docByTopicArray
    
    printf("docByTopic\n");
    for (i =  0; i < NumberOfTopics * NumberOfDocs; i++)
      printf("%ld ", docByTopic[i]);
    printf("\n");
    printf("docByTopic\n");
    for (i = 0; i < NumberOfDocs; i++){
      for (j = 0; j < NumberOfTopics; j++){
        printf("%ld ", docByTopicArray[i][j]);
      };
      printf("\n");
    }
    printf("wordByTopic\n");
    for (i = 0; i < NumberOfWords; i++){
      for (j = 0; j < NumberOfTopics; j++){
        printf("%ld ", wordByTopicArray[i][j]);
      };
      printf("\n");
    }
    printf("topics\n");
    for (i = 0; i < nnz; i++){
      printf("%ld ", topics[i]);
    };
  }
  probs = (double *) malloc(NumberOfTopics * sizeof(double));
  WBETA = BETA * NumberOfWords;
  doc = 0;
  wordInstance = 0;
  for (i = 0; i < nnz; i++){
    for (v = 0; v < (int) values[i]; v++){
      while (docPtr[doc+1] <= i) doc++;
      topic = topics[wordInstance];
      topicCount[topic]--;
      wordByTopicArray[wordID[i]][topic]--;
      docByTopicArray[doc][topic]--;

      totalprob = 0.0;

      for (j = 0; j < NumberOfTopics; j++) {
        probs[j] = ( (double) wordByTopicArray[wordID[i]][j] + BETA)/( (double) topicCount[j]+ WBETA)*( (double) docByTopicArray[doc][j]+ ALPHA);
        totalprob += probs[j];
      }

      r = myrand()*totalprob;
      max = probs[0];
      j = 0;

      while (r>max) {
        j++;
        max += probs[j];
      }

      topics[wordInstance] = j;
      wordByTopicArray[wordID[i]][j]++;
      docByTopicArray[doc][j]++;
      topicCount[j]++;
      wordInstance++;
    };
  };
  free(probs);

  return (double)( 1.0 );
}
//extern "C" __declspec(dllexport) int setMTSeed(int RandomSeed);


DllExport double setMTSeed(int RandomSeed){
  unsigned int SeedU = (unsigned int) RandomSeed;
  seedMT(SeedU); 
  return (double)(1.0);
}

}






