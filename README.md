# How to use

1. Entrez les données dans les fichiers V_H2_data.csv, V_O2_data.csv et U_or_I_data.csv
en suivant le format suivant :
```
    t, param1, param2, param3, param4
    t1, x1, x2, x3, x4
    t2, x1, x2, x3, x4
    ...
```
où la première ligne indique juste les noms des colonnes et les autres lignes contiennent les temps et les valeurs mesurées

2. Si votre paramètre est d, pH ou I, entrez les valeurs de U en fonction du temps dans le fichier U_or_I_data.csv
sinon entrez les valeurs de I en fonction du temps dans le fichier U_or_I_data.csv

3. Faites attention à ce que les temps soient les mêmes dans les 3 fichiers

4. Lancez le script graph_plotter.py et indiquez le nom du paramètre (d, pH, I ou U) dans le terminal

5. Les graphiques seront enregistrés dans le dossier Plots
