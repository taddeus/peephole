#include <stdio.h>

#define N	6

char *w[] = {"Vertalerbouw", "Ertalerbouw", "Practicum", "Optimization", "Peephole", "Eephole"};
char acron[N*2], command[100];
int  done[N], pindex[N+1];

int is_vowel(char c)
{
   return (c==65 || c==69 || c==73 || c==79 || c==85 || c==89)? 1 : 0;
}

void do_perm(int n, int done[], int index, int size)
{
   int j, i, nrv = 0, k;

   if (index == 1 && (!is_vowel(w[pindex[0]][0]) && !is_vowel(w[n][0])))
       return;
   if (index > 1) {
      nrv = is_vowel(w[pindex[index-2]][0]) +
            is_vowel(w[pindex[index-1]][0]) +
            is_vowel(w[n][0]);
      if (nrv == 0 || nrv == 3)
       return;
   }
   pindex[index++] = n;
   if (index < N && --size) {
      for (j = 0; j<N; j++) {
         if (done[j] == 0) {
            done[j] = 1;
            do_perm(j, done, index, size);
            done[j] = 0;
         }
      }
   } else {
      k = 0;
      for (i=0; i < index; i++) {
	 int t = 0;
	 while (isupper(w[pindex[i]][t]))
	    acron[k++] = w[pindex[i]][t++];
      }
      acron[k] = 0;
      printf("%s", acron);
      for (i=0; i < index; i++) 
	    printf(" %s", w[pindex[i]]);
      printf("\n");
/*      fflush(stdout); */
   }
}

int main()
{
   int i, j;

   for (j = 4; j <= N; j++) {
      for (i = 0; i < N; i++) {
        done[i] = 1;
        do_perm(i, done, 0, j);
        done[i] = 0;
      }
   }
}
