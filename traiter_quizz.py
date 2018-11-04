# -*- coding: utf-8 -*
#Installation du module xlutils
#pip install xlutils
import numpy as np
import xlrd
import datetime
import os, glob
import sqlite3

#RAZ du fichier log
f=open('log.txt','w')

conn=sqlite3.connect('psiii_quizz.db')
c=conn.cursor()

liste_quizz=['C2-1']
liste_quizz=['C1-2']

for q in liste_quizz:
    #Determination des donnees du quiz
    c.execute("SELECT idquiz, nbr_question FROM quiz WHERE nom_quiz='"+q+"'")
    (id_quiz,nbr_question)=c.fetchone()
    path=r"/Users/emiliendurif/Documents/prepa/PSI/quiz/"+q+".xlsx"
    classeur=xlrd.open_workbook(path)
    feuilles=classeur.sheet_names()
    #Ouverture de la feuille du quiz
    for f in feuilles:
        if "Sheet1" in f:
            fs=classeur.sheet_by_name(f)
        
    #Detection de la premier ligne
    i=0
    while 'Student' not in fs.cell_value(i,0):
        i+=1
    i+=1
    #i indice de la premiere ligne de donnee
    #Balayage des lignes de donnees
    while 'Class' not in fs.cell_value(i,0):
        nom=fs.cell_value(i,0)
        score=fs.cell_value(i,3)
        c.execute("SELECT idetudiant FROM etudiants WHERE lower(Nom)=lower('"+nom+"')")
        idetudiant=c.fetchone()
        print(idetudiant)
        c.execute("INSERT INTO joue (idetudiant,idquiz,score) VALUES ("+str(idetudiant[0])+","+str(id_quiz)+","+str(score)+")")
        i+=1
        #c.fetchone()
conn.commit()
conn.close()

req_score="select nom, prenom, sc_total from (select nom, prenom, sum(score) as sc_total from (select nom, prenom, score from etudiants join joue on etudiants.idetudiant=joue.idetudiant) group by nom) order by sc_total DESC"


      
                    

