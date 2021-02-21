nr_stari = int(input("Introduceti numarul de stari: "))
nr_tranz = int(input("Introduceti numarul de tranzitii: "))
alf = input("Introduceti alfabetul (fara spatiu): ")
v_fin = input("Introduceti starile finale (cu virgula): ")
st_in = input("Introduceti starea initiala: ")
       
matrix = [""]*100
lista = []

# citim tranzitiile:
print("Cititi tranzitiile: ")
for i in range(nr_tranz):
    a=input().split();
    st_prec=a[0]
    ch=a[1]
    st_urm=a[2]
    lista.append((st_prec, ch, st_urm))

AFD = []
coada_stari = []
coada_stari.append(st_in)

afd_fin = []
st = dr = 0
pos = -1
while st <= dr: 
    for ch_index in range(len(alf)):  #pentru fiecare litera din alfabet
        stare_in = coada_stari[st]  
        pos = pos + 1
        for x in coada_stari[st]:
            for nr in range(nr_tranz):
                if x == lista[nr][0] and alf[ch_index] == lista[nr][1]:
                    if matrix[pos].find(lista[nr][2]) == -1:
                        matrix[pos] = matrix[pos] + lista[nr][2]
        if matrix[pos] != "":
            AFD.append((coada_stari[st], alf[ch_index], matrix[pos]))
        if matrix[pos] not in coada_stari:
            coada_stari.append(matrix[pos])
            ok = 0
            for x in range(len(matrix[pos])):
                if matrix[pos][x] in v_fin.split(","):
                    ok = 1
            if ok ==1:
                afd_fin.append(matrix[pos])
            if stare_in == st_in and st_in in v_fin.split(",") and st_in not in afd_fin:
                afd_fin.append(st_in)
            dr = dr + 1
    st = st + 1

print(AFD)
print("Stari finale: ", end=" ")
print(afd_fin)
print("Starea initiala: " , st_in)
  