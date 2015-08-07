#!/usr/bin/env python
# encoding: utf-8
"""
Pour lire les fichiers CSV Jasco

Created by Marc-André on 2012-09-26.
Copyright (c) 2012 IGBMC. All rights reserved.
"""

import numpy as np
import matplotlib.pyplot as plt
import codecs

def load(fich):
    "lit un fichier csv"
    data = []
    meta = {}
    xydata = False
    for lin in codecs.open(fich, "rb", "latin_1"):
        lin = lin.replace(',','.').strip()
        linspl = lin.split(';')
        if linspl == ['']:       # marque la fin des données
            xydata = False
            
        if xydata:               # on est dans les données
            flin = [ float(i) for i in linspl]
            data.append(flin)

        elif len(linspl) >1 :                   # ou pas   un champs a recuperer
            meta[linspl[0]] = ";".join(linspl[1:])

        if linspl == ["XYDATA"]:   # marque le début des données
            xydata = True
    return np.array(data), meta

def decoupe(d):
    "extrait les colonnes de données"
    ldo = d[:,0]
    cd = d[:,1]
    volt = d[:,2]
    absorb = d[:,3]
    return (ldo, cd, volt, absorb)
    
def plotabs(fich, tampon=None, lincor=False):
    "dessine l'absorbace dans un fichier, supprime une composante linéaire"
    d,meta = load(fich)
    (ldo, cd, volt, absorb) = decoupe(d)
    if tampon:
        dtamp,metatamp = load(tampon)
        (a, b ,c , absorb_tamp) = decoupe(dtamp)
        absorb = absorb-absorb_tamp
        rem = " - corrected"
    else:
        rem = ""
    if lincor:      # on corrige une composante linéaire, évaluée sur les premiers points
        zone = int(0.1*len(ldo))
        fit = np.polyfit(ldo[0:zone], absorb[0:zone], 1)
        absorb = absorb-np.polyval(fit, ldo)
    print meta['Comment']
    plt.plot(ldo, absorb, label=fich+rem)
    plt.legend()
    plt.title(fich)


######################################################
def example1():
    plotabs("D2T_T35_120919a-1.csv")
    plotabs("D2T_T35_120919a-2.csv")
    plotabs("D2T_T35_120919a-1.csv", "D2T_T35_120919a-2.csv")

def example2():
    plotabs("D2T_T35_120919a-1.csv", "D2T_T35_120919a-2.csv")
    plotabs("D2T_T70_120919b-1.csv", "D2T_T70_120919b-2.csv")
    plotabs("D2T_T90_120919c-1.csv", "D2T_T90_120919c-2.csv")

def example3():
    plotabs("ThermalDenat_120919/PNA_120919_ThermDenat-1-215nm-cell 2.csv","ThermalDenat_120919/PNA_120919_ThermDenat-1-215nm-cell 1.csv",lincor=True)

if __name__ == '__main__':
    example3()
    plt.show()
    

