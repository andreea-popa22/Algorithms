#include <iostream>
#include <string>
using namespace std;

int nr_stari, nrAlfIn, nrAlfSt, nr_tranz;
char stari[100], st_in, alfIn[100], alfSt[100], Z0, s1[100], lit[100], st1[100], s2[100];
string cuv, st2[100];

void citire() {
  int i;
  cin >> nr_stari;      //numarul de stari
  for (i = 0; i < nr_stari; i++) {
    cin >> stari[i];
  }
  cin >> nrAlfIn;       //numarul de caractere din alfabetul de intrare
  for (i = 0; i < nrAlfIn; i++) {
    cin >> alfIn[i];
  }
  cin >> nrAlfSt;        //numarul de caractere din alfabetul stivei
  for (i = 0; i < nrAlfSt; i++) {
    cin >> alfSt[i];
  }
  cin >> st_in;          //starea initiala
  cin >> Z0;             //simbolul initial de pe stiva
  cin >> nr_tranz;       //numarul de tranzitii
  for (i = 0; i < nr_tranz; i++) {
    cin>>s1[i]>>lit[i]>>st1[i]>>s2[i]>>st2[i];
  }
}

int verifica(char stare, string cuv, string stiva) {
  int j;
  string stiva2, s;
  if ((cuv == "")&&(stiva == ""))
  	  return 1;
  else {
    j = 0;
    while (j<nr_tranz) {
      if (lit[j] == '~') {
        if ((stare==s1[j])&&(stiva[0]==st1[j])) {  //daca starea in care ne aflam face parte dintr-o tranzitie si in varful stivei este starea urmatoare corespunzatoare
          s = stiva.substr(1);  //pastram ce e in stiva, mai putin elementul din varf
          if (!(st2[j] == "~"))
            stiva2 = st2[j];  //daca caracterul nu e lambda, adaugam starea in varf (urmeaza concatenarea)
          else
            stiva2 = "";  //daca e lambda, nu adaugam nimic
          stiva2 += s;
          if (verifica(s2[j], cuv, stiva2))
            return 1;
        }
        if ((stare==s1[j])&&(st1[j]=='~')) {  //daca starea in care ne aflam face parte dintr-o tranzitie iar caracterul este lambda
          s = stiva;  //repetam pasii anteriori, fara a adauga in varful stivei
          if (!(st2[j] == "~"))  //daca si al doilea caracter este lambda, atunci nici nu stergem din stiva
            stiva2 = st2[j];
          else
            stiva2 = "";
          stiva2 += s;
          if (verifica(s2[j], cuv, stiva2))
            return 1;
        }
      }
      if ((stare==s1[j])&&(cuv[0]==lit[j])&&(st1[j]=='~')) {  //daca starea in care ne aflam si litera curenta corespund tranzitiei si pe stiva "stergem" lambda
        s = stiva;
        if (!(st2[j] == "~"))  //daca ce adaugam e diferit de lambda
          stiva2 = st2[j];     //salvam in stiva2
        else
          stiva2 = "";          //daca e lambda, nu adaugam nimic
        stiva2 += s;
        if (verifica(s2[j], cuv.substr(1), stiva2))
          return 1;
      }
      if ((stare==s1[j])&&(cuv[0]==lit[j])&&(stiva[0]==st1[j])) {  //daca starea in care ne aflam si litera curenta corespund tranzitiei iar varful stivei corespunde cu ce trebuia sa stergem
        s = stiva.substr(1);  //salvam ce e pe stiva, mai putin varful
        if (st2[j] != "~")    //repetam pasii anteriori
          stiva2 = st2[j];
        else
          stiva2 = "";
        stiva2 += s;
        if (verifica(s2[j], cuv.substr(1), stiva2))
          return 1;
      }
      j++;
    }
  }
  return 0;
}


int main ()
{
    string stiva;
    citire();
    cin >> cuv;   //citim cuvantul pe care vrem sa il verificam
    stiva = Z0;   //simbolul intial al stivei
    if (verifica(st_in, cuv, stiva))   //apelam functia
      cout << endl << cuv << " --> ACCEPTAT\n";
    else
      cout << endl << cuv << " --> NEACCEPTAT\n";
    return 0;
}
