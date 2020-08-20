
/* file: spsvd.i */
%module spsvd
%{

#include "svdlib.h"
extern "C" __declspec(dllexport) double get_vectorSpace( long dimensions, long iterations, long n_types, long n_docs, long nnz, long *docPtr, long *wordID, double *weightings, double *ut , double *sing, double *vt  );
%}
%include "svdlib.h"
%include spsvd.cpp
%include "carrays.i"
%array_class(long, longArray);
%array_class(double, doubleArray);
%include "windows.i"



