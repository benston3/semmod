#ifdef __cplusplus
 extern "C" {


#endif

#ifndef INLINE
# define INLINE extern inline
#endif


typedef unsigned long uint32;

#define N              (624)                 // length of state vector


static uint32   state[N+1];     // state vector + 1 extra to not violate ANSI C
static uint32   *next;          // next random value is computed from here
static int      left = -1;      // can *next++ this many times before reloading


void seedMT(uint32 seed);

uint32 reloadMT(void);

INLINE uint32 randomMT(void);

 #ifdef __cplusplus
 }
 #endif