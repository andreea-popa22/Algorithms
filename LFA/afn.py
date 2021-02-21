f=open("input.txt", "r")

nr_stari = int(f.readline().strip('\n'))
nr_tranz = int(f.readline().strip('\n'))
alf = f.readline().strip('\n')
v_fin = f.readline().strip('\n')
st_in = int(f.readline().strip('\n'))

AFN = {}
l_fin = v_fin.split()    #lista cu starile finale

for i in range(nr_stari):
    AFN.update({i:[]})
    for j in range(len(alf)):
        AFN[i].append([])      #folosesc un dictionar in care cheile sunt starile automatului
                               #iar valoarea fiecare chei este o lista mare ce contine liste cu starile in 
                               #care se poate ajunge cu litera ce are pozitia in alfabet egala cu pozitia
                               #listei de stari in lista mare

# citim tranzitiile:
print("Cititi tranzitiile: ")
for i in range(nr_tranz):
    a=f.readline().split();
    stare1=int(a[0])
    litera=a[1]
    stare2=int(a[2])
    pos = alf.find(litera)     #salvam pozitia in alfabet pentru a sti ce index are lista (in lista mare)
                               #in care trebuie sa adaugam starea2
    AFN[stare1][pos].append(stare2)
    
for i in range(nr_stari):
    print(AFN[i])
    
cuv = f.readline().strip('\n')
ok = 1

def afn(stare, cuvant):
    if cuvant == "":        #daca am ajuns la stringul vid, inseamna ca am verificat toate literele
        for x in l_fin:     #verificam daca starea in care am ajuns este finala
            if stare == int(x):
                return 1
    else:
        litera = cuvant[0:1]    #litera curenta
        pos = cuv.find(litera)    #pozitia literei in cuvant
        i = alf.find(litera)     #pozitia literei in alfabet
        l = AFN[stare][i]        #lista de stari in care se poate ajunge din starea in care eram cu litera curenta
        if l != []:              #daca nu este vida, inseamna ca exista tranzitii
            ramas = cuvant[1:]   #ne pregatim sa verificam urmatoarele litere
            for st in l:             #pentru fiecare stare din lista
                if afn(st, ramas):    #apelam functia
                    return 1
        return 0
    

for l in cuv:
    if alf.find(l) == -1:    #inainte sa apelam functia verificam daca toate literele din cuvant sunt din alfabet
        ok = 0        #daca gasim o litera care nu e in alfabet, stim deja ca acel cuvant nu apartine limbajului
if ok == 1:           #daca toate literele sunt din alfabet, apelam functia
    ok = afn(st_in, cuv)
if ok == 1:
    print("cuvant acceptat")
else:
    print("cuvant neacceptat")

