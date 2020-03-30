#include <stdio.h>
#include <stdlib.h>
#include "math.h"

double ** readfile(char *name, int *nx, int *ny)
{
	FILE * pFile;
	long lSize;
	char * buffer;
	size_t result;
	double **ms;
	
	pFile = fopen (name,"r");
	if (pFile==NULL) {fputs ("File error",stderr); exit (1);}
	
	fseek (pFile , 0 , SEEK_END);
	lSize = ftell (pFile);
	rewind (pFile);

	buffer = (char*) malloc (sizeof(char)*lSize);
	if (buffer == NULL) {fputs ("Memory error",stderr); exit (2);}

 	result = fread (buffer,1,lSize,pFile);
 	if (result != lSize) {fputs ("Reading error",stderr); exit (3);}

	*nx = 0;
	*ny = 0;
	int k = 0;

	for(int i = 0; i < lSize; i++)
	{
		if (k == 0){
			if (buffer[i] == ' '){
				*nx += 1;
			}
		}
		if (buffer[i] == '\n'){
			*ny += 1;
			k += 1;
		}
	}
	
	*nx += 1;
	*ny += 1;
	printf("NX=%d\tNY=%d\n", *nx, *ny);
	
	ms = (double **) malloc(*ny*sizeof(double *));
	for(int i = 0; i < *ny ; i++){ ms[i] = (double *) malloc(*nx*sizeof(double)); }

	char s[20];
	for(int i = 0; i < 20; i++){s[i] = ' ';}
	int is = 0;
	int ix = 0;
	int iy = 0;
	for(int i = 0; i < lSize; i++){
		if (buffer[i] != ' ' && buffer[i] != '\n'){
			s[is] = buffer[i];
			is++;
		}
		else{
			if (buffer[i] != '\n'){
				ms[iy][ix] = atof(s);
				for(int j = 0; j < is; j++){s[j] = ' ';}
				ix++;
				is = 0;
			}
			else{
				ms[iy][ix] = atof(s);
				for(int j = 0; j < is; j++){s[j] = ' ';}
				ix = 0;
				is = 0;
				iy++;
			}
		}
	}

	ms[*ny-1][*nx-1] = atof(s);

  	fclose (pFile);
	free (buffer);
	return ms;
}

int main(int argc, char *argv[])
{
	double **mass;
	int nc,ns;
	double pi = 4.*atan(1.0);
	double* xx;
	double* yy;
	double power,shift,freq,dt,t,f_max,f_min,df,campl,vampl,uampl,s1,s2;
	double dt_min = 1.e10;

	mass = readfile(argv[1],&nc,&ns);
	xx = (double*) malloc(ns*sizeof(double));
	yy = (double*) malloc(ns*sizeof(double));

	for(int i = 0; i < ns; i++){
		xx[i] = mass[i][0];
		yy[i] = mass[i][3];}

	for(int i = 0; i < ns - 1; i++){
		dt = xx[i+1] - xx[i];
		if(dt < dt_min){ dt_min = dt; }
		}

	t = xx[ns-1] - xx[0];
	f_max = 1/(2*dt_min);
	f_min = 1/(2*t);	
	df = (f_max - f_min)/((double) ns);
	printf("FMAX=%.4f\tFMIN=%.8f\tDF=%.8f\n",f_max,f_min,df);

	for(int i = 0; i < ns; i++){ 
		campl = 0;
		vampl = 0;
		uampl = 0;
		s1 = 0;
		s2 = 0;
		freq = f_min + df*((double) i);

		for(int j = 0; j < ns ; j++){
			s1 += sin(4.*pi*freq*xx[j]);
			s2 += cos(4.*pi*freq*xx[j]);}
		shift = atan(s1/s2)/(4.*pi*freq);

		for(int j = 0; j < ns; j++){
			campl += cos(4.*pi*freq*(xx[j] - shift));
			uampl += yy[j]*cos(2.*pi*freq*(xx[j] - shift));
			vampl += yy[j]*sin(2.*pi*freq*(xx[j] - shift));}

		campl = 1 + campl/ns;
		uampl = uampl/ns;
		vampl = vampl/ns;
		
		power = (pow(uampl,2.0)/campl)+(pow(vampl,2.0)/(2.0-campl));
		printf("%g\t%g\n", freq, power);}
	

	free(xx);
	free(yy);
	free(mass);

	return 0;
}
	
	
