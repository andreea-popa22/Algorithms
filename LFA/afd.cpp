#include <iostream>
#include <cstring>

using namespace std;

int main()
{
    int nr_noduri, nr_tranz, i, j, link, st_in, v_fin[50], nr_fin, ok=1, s;
    char m[50][50], alf[50], cuv[50], ch;
    cin >> nr_noduri >> nr_tranz >> nr_fin >> alf >> cuv;
    for (i = 0; i < nr_noduri; i++)
        for (j = 0; j < int(strlen(alf)); j++)
            m[i][j] = -1;
    for (i = 0; i < nr_fin; i++){
        cin >> v_fin[i];
    }
    for (i = 0; i < nr_tranz; i++){
        cin >> st_in >> link >> ch;
        if (strchr(alf, ch) != NULL){
            m[st_in][ch] = link;
        }
        else{
            ok=0;
        }
    }
    if( ok==1){
        for(j=0;j<int(strlen(cuv));j++){
            if(j==0){
                s=m[0][cuv[j]];
            }
            else{
                s = m[s][cuv[j]];
                if(s == -1){
                    ok = 0;
                    break;
                }
            }
        }
    }
    if (ok == 0){
        cout<<"cuvant neacceptat";
    }
    else{
        ok = 0;
        for (i = 0; i < nr_fin; i++)
            if (v_fin[i] == s)
                ok = 1;
        if( ok == 1 )
            cout<<"cuvant acceptat";
        else
            cout<<"cuvant neacceptat";
    }

    return 0;
}
