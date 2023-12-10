import tkinter as tk
import datetime as dt
import mysql.connector
import logique as log
from logique import Tache
from tkinter import messagebox
from tkinter import ttk
import acceuil


#connexion à la base de données
connexion = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "",
    database = "MYBASE"
)
curseur = connexion.cursor()

def get_task():
    try:
        nom = entre_nom.get()
        temps = entre_duree.get()
        priorite = entre_oPriorite.get()
      
        if nom=="" or temps== "":
            messagebox.showerror("Erreur","Duration and name are needed")
        elif  isinstance(int(temps),int)  or   isinstance(int(priorite),int):
            messagebox.showerror("Erreur","Duration or priority must be a number")
            
        else:  
            tache = Tache(nom,temps,priorite) 
            tache.creer_tache()
            messagebox.showinfo("Task","Task was sucessfulty created")
    except Exception as e:
        messagebox.showerror("error",e)
#rechercher une tâche dans la base de 

#def affiche_tâche():
def affiche_tache():
    #connexion à la base de données
    connexion = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "",
    database = "MYBASE"
    )
    for i in mytree.get_children():
        mytree.delete(i)
    curseur = connexion.cursor()
    rq='select * from tache order by priority asc'
    curseur.execute(rq)
    resultats=curseur.fetchall()
    for row in resultats:
        mytree.insert('', index='end' ,values=row)
#fonction de recherche d'une tâche
def recherche_tache():
        #connexion à la base de données
    connexion = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "",
    database = "MYBASE"
    )
    for i in mytree.get_children():
        mytree.delete(i)
    curseur = connexion.cursor()
    nom = entree_recherche.get()
    req = "select * from tache where name=%s"
    val=(nom,)
    curseur.execute(req,val)
    resultat=curseur.fetchall()
    if not resultat:
        messagebox.showinfo("research",'task not found')
    else:
        for row in resultat:
            
            mytree.insert('',index='end',values=row)
            print(row)
# affichage de tache en cours
def tache_en_cours():
    try:
                    #connexion à la base de données
        connexion = mysql.connector.connect(
        host = "127.0.0.1",
        user = "root",
        password = "",
        database = "MYBASE"
        )
        for i in mytree.get_children():
            mytree.delete(i)
        curseur = connexion.cursor()
        
        req = "select *from tache where state=%s"
        val = ("en cours",)
        curseur.execute(req,val)
        resultats=curseur.fetchall()
        for row in resultats:
            mytree.insert('',index='end',values=row)
    except Exception as e :
        messagebox.showerror('erreur',e)
        
#effacer une tache
def delete_tache():
    1+1
          
fenetre1 = tk.Tk()
fenetre1.title("TASKS MANAGER")
fenetre1.configure(background="white")
fenetre1.geometry("1000x1000")
#création du menu qui permettra la visualisation des différentes tâches

menu1 =tk.Menu(fenetre1, background="skyblue")
listeT = tk.Menu(menu1, tearoff=0, background="skyblue")
listeT.add_command(label="All tasks",command=affiche_tache)
listeT.add_command(label="Tâches en cours",command=tache_en_cours)
listeT.add_command(label="Tâches terminées")
menu1.add_cascade(label="Tâches", menu=listeT, font=("Sans serif" ,15))
        
fenetre1.config(menu=menu1) 
        
#création du formulaire pour la création d'une tâche

formulaire = tk.Frame (fenetre1 , height="750", width="750", background="skyblue")
formulaire.place(x=0,y=50)
# ici je donne un titre au formulaire 

titre_formulaire = tk.Label(formulaire,text="Enter task details",borderwidth = 5,font=("Sans serif",20),relief="sunken", bg='white')
titre_formulaire.place(x = 0, y = 0, width = 750,height =35)

#champs de saisie du nom de la tâche

nom_tache = tk.Label(formulaire,text="Task name",font=("Arial",12), background="skyblue")
nom_tache.place(x=5,y=60 ,width=250)
entre_nom = tk.Entry(formulaire,font=("Arial",12),bd=3, justify='center')
entre_nom.place(x=300,y=60,width=400)

#champs de saisie de la durée potentielle de la tâche

duree_tache = tk.Label(formulaire,text="Task duration (s):",font=("Arial",12), background="skyblue")
duree_tache.place(x=5,y=120 ,width=250)
entre_duree = tk.Entry(formulaire,font=("Arial",12),bd=3, justify='center')
entre_duree.place(x=300,y=120,width=400)

#champs de saisie de l'ordre de priorité de la tâche

oPriorite_tache = tk.Label(formulaire,text="Task priority",font=("Arial",12), background="skyblue")
oPriorite_tache .place(x=5,y=180 ,width=270)
entre_oPriorite = tk.Entry(formulaire,font=("Arial",12),bd=3, justify='center')
entre_oPriorite .place(x=300,y=180,width=400)

#création de bouton

bouton_create = tk.Button(formulaire, background="white", font=("Sans serif",12), text= "Create", command=get_task)
bouton_create.place(x=300, y=300, width= 100)
mytree = ttk.Treeview(fenetre1,columns=(1,2,3,4,5,6),show="headings",height=5)
mytree.place(x=750,y=50,width=780,height=1500)
# bouton modifier
bouton_modifier = tk.Button(formulaire, background="white", font=("Sans serif",12), text= "Modify")
bouton_modifier.place(x=50, y=400, width= 100)
#bouton de suppression
bouton_supprimer = tk.Button(formulaire, background="white", font=("Sans serif",12), text= "Delete")
bouton_supprimer .place(x=500, y=400, width= 100)
#bouton d'abandon
bouton_abandon= tk.Button(formulaire, background="white", font=("Sans serif",12), text= "Abandon")
bouton_abandon.place(x=300, y=600, width= 100)
#création des entêtes
mytree.heading(1,text="ID")
mytree.heading(2,text="NAME")
mytree.heading(3,text="DURATION")
mytree.heading(4,text="PRIORITY")
mytree.heading(5,text="DATE")
mytree.heading(6,text="STATE")
#formatage des colonnes
mytree.column(1,width=120)
mytree.column(2,width=120)
mytree.column(3,width=120)
mytree.column(4,width=120)
mytree.column(5,width=120)
mytree.column(6,width=120)
#création des éléments du champs de recherche
entree_recherche = tk.Entry(fenetre1,font=("Sans serif",12), bd=3,  justify='center')
entree_recherche.place(x=600, y=10, width=300,height=30)
bouton_recherche = tk.Button(fenetre1, background="skyblue", font=("Sans serif",12), text="Research", relief='flat',command=recherche_tache)
bouton_recherche.place(x=910, y=10, width= 100, height=27)

if __name__=="__main__":
    
    acceuil.fenetre2.mainloop()
 
    


                    