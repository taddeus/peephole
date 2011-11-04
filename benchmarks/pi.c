#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
   int i, its, hits = 0;
   double d1, d2;

   if (argc != 2) {
      fprintf(stderr, "Usage: %s <iterations>\n", argv[0]);
      exit(0);
   }

   its = atoi(argv[1]);
   srandom(1);
   for (i = 0; i < its; i++) {
      d1 = ((double)random())/2147483647.0;
      d2 = ((double)random())/2147483647.0;
      if (((d1*d1) + (d2*d2)) <= 1)
	 hits++;
   }
   printf("%.10f\n", (double)4.0 * (double) ((double)hits / (double)its));
   return 1;
}

