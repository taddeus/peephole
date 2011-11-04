#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

/*
timer program -- computes total time in seconds
since the first call. Uses constant CLOCK_RATE
to compute of CPU time in seconds
*/
/* Unix clock */
#define CLOCK_RATE 1000000.0

/* MS-DOS Turbo C 
#define CLOCK_RATE CLK_TCK
*/
float second(void);

float second()
{
   return((float)clock() / CLOCK_RATE);
}

/* C-style global parameters */

float T,T1,T2,E1[4];
int J,K,L;

void POUT(long n, long j, long k, float x1, float x2, float x3, float x4)
{
	printf("\n %7.1ld%7.1ld%7.1ld%12.4e%12.4e%12.4e%12.4e%8.2f",
	n,j,k,x1,x2,x3,x4,second());
}

void PA(E)
float *E;
{
	int j;
	j=0;
	do {
		E[0]=(E[0]+E[1]+E[2]-E[3])*T;
		E[1]=(E[0]+E[1]-E[2]+E[3])*T;
		E[2]=(E[0]-E[1]+E[2]+E[3])*T;
		E[3]=(-E[0]+E[1]+E[2]+E[3])/T2;
		j=j+1;
	}
	while(j<6);
}

void P0()
{
	E1[J-1]=E1[K-1];
	E1[K-1]=E1[L-1];
	E1[L-1]=E1[J-1];
}

void P3(X, Y, Z)
float *X, *Y, *Z;
{
	float X1, Y1;

	X1=*X;
	Y1=*Y;
	X1=T*(X1+Y1);
	Y1=T*(X1+Y1);
	*Z=(X1+Y1)/T2;
}

/* equivalent description of FORTRAN-style common block ( slow !) */
/*
struct _comm_blk_ {
	float _T, _T1, _T2, _E1[4];
	int _J,_K,_L;
} common;
#define T common._T
#define T1 common._T1
#define T2 common._T2
#define E1 common._E1
#define J common._J
#define K common._K
#define L common._L
*/

int main()
{
float X1,X2,X3,X4,X,Y,Z;
long I,ISAVE,N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N11,N12;

	printf("Start timing.");

	I = 10;
	T1=0.50025000;
	T=0.499975000;
	T2=2.0000;
	ISAVE=I;
	N1=0;
	N2=12*I;
	N3=14*I;
	N4=348*I;
	N5=0;
	N6=210*I;
	N7=32*I;
	N8=899*I;
	N9=516*I;
	N10=0;
	N11=93*I;
	N12=0;
	X1=1.0;
	X2=-1.0;
	X3=-1.0;
	X4=-1.;
	for(I=0; I<N1; I++)
	{
		X1=(X1+X2+X3-X4)*T;
		X2=(X1+X2-X3+X4)*T;
		X4=(-X1+X2+X3+X4)*T;
		X3=(X1-X2+X3+X4)*T;
	}
	POUT(N1,N1,N1,X1,X2,X3,X4);
	E1[0]=1.0;
	E1[1]=-1.0;
	E1[2]=-1.0;
	E1[3]=-1.0;
	for(I=0; I<N2; I++)
	{
		E1[0]=(E1[0]+E1[1]+E1[2]-E1[3])*T;
		E1[1]=(E1[0]+E1[1]-E1[2]+E1[3])*T;
		E1[2]=(E1[0]-E1[1]+E1[2]+E1[3])*T;
		E1[3]=(-E1[0]+E1[1]+E1[2]+E1[3])*T;
	}
	POUT(N2,N3,N2,E1[0],E1[1],E1[2],E1[3]);

	for(I=0; I<N3; I++) PA(E1);
	POUT(N3,N2,N2,E1[0],E1[1],E1[2],E1[3]);
	J=1;

	for(I=0; I<N4; I++)
	{
		if(J==1) J=2;
		else J=3;

		if(J<2) J=0;
		else J=1;

		if(J<1) J=1;
		else J=0;
	}
	POUT(N4,J,J,X1,X2,X3,X4);
	J=1;
	K=2;
	L=3;
	for(I=0; I<N6; I++)
	{
		J=J*(K-J)*(L-K);
		K=L*K-(L-J)*K;
		L=(L-K)*(K+J);
		E1[L-2]=J+K+L;
		E1[K-2]=J*K*L;
	}
	POUT(N6,(long)J,(long)K,E1[0],E1[1],E1[2],E1[3]);

	X=0.5;
	Y=0.5;
	{
	 register float x=X;
	 register float y=Y;
	 register float t2=T2;
	 register float t=T;

	 for(I=0; I<N7; I++)
	 {
		x=t*atan(t2*sin(x)*cos(x)/(cos(x+y)+cos(x-y)-1.0));
		y=t*atan(t2*sin(y)*cos(y)/(cos(x+y)+cos(x-y)-1.0));
	 }
	 X=x; Y=y;
	}
	POUT(N7,(long)J,(long)K,X,X,Y,Y);
	X=1.0;
	Y=1.0;
	Z=1.0;

	for(I=0; I<N8; I++) P3(&X,&Y,&Z);
	POUT(N8,(long)J,(long)K,X,Y,Z,Z);
	J=1;
	K=2;
	L=3;
	E1[0]=1.0;
	E1[1]=2.0;
	E1[2]=3.0;
	for(I=0; I<N9; I++) P0();
	POUT(N9,(long)J,(long)K,E1[0],E1[1],E1[2],E1[3]);
	J=2;
	K=3;
	for(I=0; I<N10; I++)
	{
		J+=K;
		K+=J;
		J-=K;
		K-=J+J;
	}
	POUT(N10,(long)J,(long)K,X1,X2,X3,X4);
	X=0.75;
	{
	 register float x=X;
	 register float t1=T1;
	 for(I=0; I<N11; I++) 	x=sqrt(exp(log(x)/t1));
	 X=x;
	}
	POUT(N11,(long)J,(long)K,X,X,X,X);

	printf("\n %g whetstones per second\n", 1.0e+08/second());
}

