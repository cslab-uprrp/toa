#include <cmath>
#include <stdio.h>
#include <iostream>

using namespace std;

double funcion1(double angulo1, double long1, double long2){
	
	return asin(sin(angulo1)*(long1/long2));

}

double funcion2(double valorfuncion1){
	
	cout<<endl<<valorfuncion1<<endl;

	return valorfuncion1 - 1;

}

double funcion3(double valorfuncion2){

	cout<<endl<<valorfuncion2<<endl;

	return valorfuncion2 - 1;

}



int main(){

	double input1, input2, input3;

	cout<<endl<<"Enter values: Ej. value1, value2, value3";

	cin>>input1>>input2>>input3;

	cout<<endl<<input1<<", "<<input2<<", "<<input3<<endl;
	
	double resultado = funcion3(funcion2(funcion1(angulo, long_1, long_2)));

}
