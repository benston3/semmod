// spsvd.cpp : Defines the entry point for the DLL application.
//



#include "svdlib.h"
#include "svdutil.h"

#include <stdio.h>
#include <stdlib.h>
#include "stdafx.h"

long RandomSeed;

extern "C" __declspec(dllexport) int _spsvd( long dimensions, long iterations, long n_types, long n_docs, long nnz, long RSeed, int *docPtr, int *wordID, double *weightings, double *ut, double *sing, double *vt  );

int _spsvd( long dimensions, long iterations, long n_types, long n_docs, long nnz, long RSeed, int *docPtr, int *wordID, double *weightings, double *ut, double *sing, double *vt  );


BOOL APIENTRY DllMain( HANDLE hModule, 
                       DWORD  ul_reason_for_call, 
                       LPVOID lpReserved
					 )
{
    return TRUE;
}



void setRandomSeed(long Seed){
  RandomSeed = Seed;
}

int getRandomSeed(void){
  return((int)RandomSeed);
}

DMat svdNewDMatFromPointer(int rows, int cols, double *memptr);

DMat svdNewDMatFromPointer(int rows, int cols, double *memptr) {
  int i;
  DMat D = (DMat) malloc(sizeof(struct dmat));
  if (!D) {perror("svdNewDMat"); return NULL;}
  D->rows = rows;
  D->cols = cols;

  D->value = (double **) malloc(rows * sizeof(double *));
  if (!D->value) {SAFE_FREE(D); return NULL;}

  D->value[0] = memptr;
  if (!D->value[0]) {SAFE_FREE(D->value); SAFE_FREE(D); return NULL;}

  for (i = 1; i < rows; i++) D->value[i] = D->value[i-1] + cols;
  return D;
}

int _spsvd( long dimensions, long iterations, long n_types, long n_docs, long nnz, long RSeed, int *docPtr, int *wordID, double *weightings, double *ut, double *sing, double *vt  )
{
  int i, j;
   /* Set random seed */
  setRandomSeed(RSeed);
 
  if (FALSE){
    printf("In _spsvd\n"); fflush(stdout);
    printf("dimensions = %d\n", dimensions); fflush(stdout);
    printf("iterations = %d\n", iterations); fflush(stdout);
    printf("n_types = %d\n", n_types); fflush(stdout);
    printf("n_docs = %d\n", n_docs); fflush(stdout);
    printf("nnz = %d\n", nnz); fflush(stdout);
    // print docPtr
    for (i = 0; i < n_docs+1; i++)
       printf("%d ", docPtr[i]);
    printf("\n"); fflush(stdout);
    // print wordID
    for (i = 0; i < nnz; i++)
       printf("%d ", wordID[i]);
    printf("\n"); fflush(stdout);
    // print weightings
    for (i = 0; i < nnz; i++)
       printf("%f ", weightings[i]);
    printf("\n"); fflush(stdout);
    //  print ut
    for (i = 0; i < nnz /*n_types*dimensions */; i++){
       printf("%f ", ut[i]); fflush(stdout);
    };
    printf("\n"); fflush(stdout);
  };
  

  double las2end[2] = {-1.0e-30, 1.0e-30};
  double kappa = 1e-6;

  SVDRec R;

  SMat A;
  A = svdNewSMat(n_types, n_docs, nnz); 

  A->rows = n_types;
  A->cols = n_docs;
  A->vals = nnz;     /* Total non-zero entries. */
  A->pointr = (long *) docPtr;  /* For each col (plus 1), index of first non-zero entry. */
  A->rowind = (long *) wordID;  /* For each nz entry, the row index. */
  A->value = weightings; /* For each nz entry, the value. */

  R = svdNewSVDRec();
  R->Ut = svdNewDMatFromPointer(dimensions, n_types, ut);
  R->Vt = svdNewDMatFromPointer(dimensions, n_docs, vt);
  R->S = sing;
  R->d  = dimensions;

  svdLAS3(A, dimensions, iterations, las2end, kappa, R); 

  return(1);
}
