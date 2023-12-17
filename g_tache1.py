import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import datetime as dt
from datetime import date
from datetime import datetime
import tkcalendar as tkc 
#ici nous allons créer une classe tâche qui prendra une fenêtre en paramètre


class Tache:
    def __init__(self,fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Tasks manager")
        self.fenetre.geometry("1800x850")

        
        #création du menu qui permettra la visualisation des différentes tâches

        menu1 =tk.Menu(self.fenetre, background="skyblue")
        listeT = tk.Menu(menu1, tearoff=0, background="skyblue")
        listeT.add_command(label="All tasks",command=self.screen_all)
        listeT.add_command(label="Oder by deadline",command=self.screen_all_dead)
        listeT.add_command(label="Order by priority",command=self.screen_all_p)
        listeT.add_command(label="Oder by state",command=self.screen_all_S)
        listeT.add_command(label="Late tasks",command=self.screen_all_late)
        menu1.add_cascade(label="Tasks", menu=listeT, font=("Sans serif" ,15))
        self.fenetre.config(menu=menu1) 
                
        #ici nous allons créer un frame qui va conteni notre formulaire de création de tâche
        self.formulaire = tk.Frame (self.fenetre, height="500", width="600", background="skyblue")
        self.formulaire.place(x=0,y=50)
        self.titre_formulaire = tk.Label(self.formulaire,text="Enter task details",borderwidth = 5,font=("Sans serif",20),relief="sunken", bg='white')
        self.titre_formulaire.place(x = 0, y = 0, width = 500,height =35)
        #champs de saisie du nom de la tâche

        self.nom_tache = tk.Label(self.formulaire,text="Task name",font=("Arial",12), background="skyblue")
        self.nom_tache.place(x=0,y=60 ,width=250)
        self.entre_nom = tk.Entry(self.formulaire,font=("Arial",12),bd=3, justify='center')
        self.entre_nom.place(x=300,y=60,width=290)

#champs de saisie de la date de debut de la tâche

        self.date_debut = tk.Label(self.formulaire,text="Date",font=("Arial",12), background="skyblue")
        self.date_debut.place(x=0,y=120 ,width=250)
        self.entre_date_debut = tkc.DateEntry(self.formulaire,font=("Arial",12),bd=3, justify='center',date_pattern='yyyy-mm-dd')
        self.entre_date_debut.place(x=300,y=120,width=290)
        
#champs de saisie de la date de fin

        self.date_fin = tk.Label(self.formulaire,text="Deadline",font=("Arial",12), background="skyblue")
        self.date_fin.place(x=0,y=180 ,width=250)
        self.entre_date_fin = tkc.DateEntry(self.formulaire,font=("Arial",12),bd=3, justify='center',date_pattern='yyyy-mm-dd')
        self.entre_date_fin.place(x=300,y=180,width=290)
        
#création de la base de données

        self.connexion = mysql.connector.connect(
        host = "127.0.0.1",
        user = "root",
        password = ""
)     
        self.curseur = self.connexion.cursor()
        self.curseur.execute('CREATE DATABASE IF NOT EXISTS MYBASE')
        self.curseur.execute('USE MYBASE')
        self.curseur.execute("CREATE TABLE IF NOT EXISTS TACHE (ID INT AUTO_INCREMENT PRIMARY KEY , NAME VARCHAR(25) UNIQUE NOT NULL , PRIORITY  INT DEFAULT '3', START_DATE  DATE NOT NULL , DEADLINE  DATE NOT NULL, STATE VARCHAR(25) )")
        
        
        #pour la priorité de la tâche l'utilisateur devra choisir entre les chiffres 1,2,3 la priorité 1 étant la plus élevée
        #nous ferons cela dans un menu déroulant
        self.oPriorite_tache = tk.Label(self.formulaire,text="Task priority",font=("Arial",12), background="skyblue")
        self.oPriorite_tache.place(x=0,y=240 ,width=270)
        
        liste_options = [3,2,1]
        self.option =tk.IntVar(self.formulaire)
# met 3 comme valeur par défaut du optionmenu
        self.option.set(3)
        self.liste_priorite = tk.OptionMenu(self.formulaire, self.option, *liste_options)
        self.liste_priorite.config(background="white")
        self.liste_priorite.place(x=300,y=240,width=150)
#Création du bouton d'enregistrement
        self.bouton_create = tk.Button(self.formulaire, background="white", font=("Sans serif",12), text= "Save", command=self.create_task)
        self.bouton_create.place(x=250, y=400, width= 100)
#création des treeview pour afficher les tâches
        self.mytree = ttk.Treeview(self.fenetre,columns=(1,2,3,4,5),show="headings",height=5)
        self.mytree.place(x=600,y=50,width=935,height=1500)
        
                #création des entêtes
        
        self.mytree.heading(1,text="NAME")
        self.mytree.heading(2,text="PRIORITY")
        self.mytree.heading(3,text="START DATE")
        self.mytree.heading(4,text="DEADLINE")
        self.mytree.heading(5,text="STATE")
        #formatage des colonnes
        
        self.mytree.column(1,width=120)
        self.mytree.column(2,width=120)
        self.mytree.column(3,width=120)
        self.mytree.column(4,width=120)
        self.mytree.column(5,width=120)
        #création des éléments du champs de recherche
        self.entree_recherche = tk.Entry(fenetre,font=("Sans serif",12), bd=3,  justify='center')
        self.entree_recherche.place(x=600, y=10, width=300,height=30)
        self.bouton_recherche = tk.Button(fenetre, background="skyblue", font=("Sans serif",12), text="Research", relief='flat',command=self.research_task)
        self.bouton_recherche.place(x=910, y=10, width= 100, height=27)
#bouton supprimer
        self.bouton_supprimer = tk.Button(self.fenetre,text = 'Delete',font=('Sans serif',12),relief='flat',bg="skyblue",command=self.delete_task)
        self.bouton_supprimer.place(x=350,y=600,width=100)
#bouton pour terminer une tâche

        self.bouton_terminer= tk.Button(self.fenetre,text = 'finish',font=('Sans serif',12),relief='flat',bg="skyblue",command=self.termninate_task)
        self.bouton_terminer.place(x=225,y=600,width=100)
#bouton pour modifier une tâch
        self.bouton_modifier = tk.Button(self.fenetre,text = 'Modify',font=('Sans serif',12),relief='flat',bg="skyblue",command=self.modify_task)
        self.bouton_modifier.place(x=100,y=600,width=100)
        
#bouton pour enregistrer les modifications

        self.bouton_save_modification = tk.Button(self.fenetre,text='Save modification',font=("Sans serif",12),relief='flat',bg='skyblue',command=self.save_modification)
        self.bouton_save_modification.place(x=175,y=670,width=200)
        self.screen_all()
#cette fonction récupèrera les entrées et les traitera

    def recupere(self):
            try:
                nom = self.entre_nom.get()
                date_debut = self.entre_date_debut.get_date()
                date_fin =self.entre_date_fin.get_date()
                priorite = self.option.get()
                if nom == '':
                        return[]
                elif date_debut<dt.date.today() or date_fin<dt.date.today() or date_fin<date_debut:
                        return[]
                else:
                        return[nom,priorite,date_debut,date_fin]
                        
                        
            except Exception as e:
                    messagebox.showerror('error',e)
                     
                
              
#fonction de création d'une tâche dans la base de données

    def create_task(self):
                try:
                        valeurs = self.recupere()
                        if valeurs==[]:
                                messagebox.showerror('error','fill task name or verify that dates are corrects')
                        else:
                                self.connexion = mysql.connector.connect(
                                host = "127.0.0.1",
                                user = "root",
                                password = "",
                                database = 'MYBASE'
                                )
                                self.curseur = self.connexion.cursor()
                                self.curseur.execute("SELECT * FROM TACHE WHERE NAME =%s",(valeurs[0],))
                                resultat = self.curseur.fetchall()
                                if not resultat:
                                        if valeurs[2]== dt.date.today():
                                                etat = 'running'
                                                self.curseur = self.connexion.cursor()
                                                req = 'INSERT INTO TACHE (NAME, PRIORITY, START_DATE, DEADLINE,STATE) VALUES(%s,%s,%s,%s,%s)'
                                                val = (valeurs[0],valeurs[1],valeurs[2], valeurs[3],etat)
                                                self.curseur.execute(req,val)
                                                self.connexion.commit()
                                                messagebox.showinfo("Tasks mmanager","Task was suceesfuly added")
                                        if valeurs[2]>dt.date.today():
                                                
                                                etat = 'waiting'
                                                self.curseur = self.connexion.cursor()
                                                req = 'INSERT INTO TACHE (NAME, PRIORITY, START_DATE, DEADLINE,STATE) VALUES(%s,%s,%s,%s,%s)'
                                                val = (valeurs[0],valeurs[1],valeurs[2], valeurs[3],etat)
                                                self.curseur.execute(req,val)
                                                self.connexion.commit()
                                                messagebox.showinfo("Tasks mmanager","Task was suceesfuly added")
                                        if valeurs[3]<date.today():
                                                messagebox.showerror("Error","You are trying to register a task whitch is late")                               
                                else:
                                        messagebox.showerror("error","task whith this name already exists")
                                self.screen_all()
                                
                except Exception as e:
                        messagebox.showerror('error',e)

#cette fonction permettra d'afficher toutes les taches de la base de données dans un tableau

    def screen_all(self):
            try:
                self.connexion = mysql.connector.connect(
                host = "127.0.0.1",
                user = "root",
                password = "",
                database = 'MYBASE'
                )
                for i in self.mytree.get_children():
                        self.mytree.delete(i)
                self.curseur = self.connexion.cursor()
                self.curseur.execute('SELECT * FROM TACHE')
                resultat = self.curseur.fetchall()
                for row in resultat:
                        self.mytree.insert('', index = 'end',values=(row[1],row[2],row[3],row[4],row[5]))
        
            except Exception as e:
                    messagebox.showerror('error',e)

#cette fonction permettra d'afficher les tâches ordonnées suivant l'ordre de priorité

    def screen_all_p(self):
            
        try:
                self.connexion = mysql.connector.connect(
                host = "127.0.0.1",
                user = "root",
                password = "",
                database = 'MYBASE'
                )
                for i in self.mytree.get_children():
                        self.mytree.delete(i)
                self.curseur = self.connexion.cursor()
                self.curseur.execute('SELECT * FROM TACHE ORDER BY PRIORITY ASC')
                resultat = self.curseur.fetchall()
                for row in resultat:
                        self.mytree.insert('', index = 'end',values=(row[1],row[2],row[3],row[4],row[5]))
        
        except Exception as e:
                messagebox.showerror('error',e)
                        
# cette fonction permettra d'afficher toutes les tâches par ordre en fonction de l'état 

    def screen_all_S(self):
            
        try:
                self.connexion = mysql.connector.connect(
                host = "127.0.0.1",
                user = "root",
                password = "",
                database = 'MYBASE'
                )
                for i in self.mytree.get_children():
                        self.mytree.delete(i)
                self.curseur = self.connexion.cursor()
                self.curseur.execute('SELECT * FROM TACHE ORDER BY STATE ASC')
                resultat = self.curseur.fetchall()
                for row in resultat:
                        self.mytree.insert('', index = 'end',values=(row[1],row[2],row[3],row[4],row[5]))
        
        except Exception as e:
                messagebox.showerror('error',e)     

#cette fonction permettra d'afficher toutes les tâches en retard
     
    def screen_all_late(self):
            
        try:
                self.connexion = mysql.connector.connect(
                host = "127.0.0.1",
                user = "root",
                password = "",
                database = 'MYBASE'
                )
                for i in self.mytree.get_children():
                        self.mytree.delete(i)
                self.curseur = self.connexion.cursor()
                self.curseur.execute('SELECT * FROM TACHE WHERE STATE=%s',("late",))
                resultat = self.curseur.fetchall()
                for row in resultat:
                        self.mytree.insert('', index = 'end',values=(row[1],row[2],row[3],row[4],row[5]))
        
        except Exception as e:
                messagebox.showerror('error',e)            


# cette fonction permettra d'afficher toutes les tâches par ordre en fonction de la date de fin

    def screen_all_dead(self):
            
        try:
                self.connexion = mysql.connector.connect(
                host = "127.0.0.1",
                user = "root",
                password = "",
                database = 'MYBASE'
                )
                for i in self.mytree.get_children():
                        self.mytree.delete(i)
                self.curseur = self.connexion.cursor()
                self.curseur.execute('SELECT * FROM TACHE ORDER BY DEADLINE ASC')
                resultat = self.curseur.fetchall()
                for row in resultat:
                        self.mytree.insert('', index = 'end',values=(row[1],row[2],row[3],row[4],row[5]))
        
        except Exception as e:
                messagebox.showerror('error',e)   

#cette fonction permettra de récupérer les differents champs d'un élément sélectionné dans la treevieew

    def selection_treeview(self):
            try:
                    selection = self.mytree.selection()
                    return self.mytree.item(selection,'values')
            except Exception as e:
                    messagebox.showerror('error',e)
                    
# cette fonction permettra de supprimer une tâche dans la base de données

    def delete_task(self):
            try:
                resultat = self.selection_treeview()
                self.connexion = mysql.connector.connect(
                host = "127.0.0.1",
                user = "root",
                password = "",
                database = 'MYBASE'
                )
                self.curseur = self.connexion.cursor()
                self.curseur.execute("SELECT * FROM TACHE WHERE NAME = %s",(resultat[0],))
                valeur_retournee= self.curseur.fetchone()
                if not valeur_retournee:
                        messagebox.showerror('error','Your trying to delete a task that does not exist')
                else:
                        self.curseur.execute('DELETE FROM TACHE WHERE NAME=%s',(resultat[0],))
                        messagebox.showinfo("Task","Task was successfuly delated")
                        self.connexion.commit()
                self.screen_all()        
            except Exception :
                    messagebox.showerror('error','select the task you want to delete')
 
#cette fonction permettra la recherche d'une tâche particulière                  
                   
    def research_task(self):
            try:
                self.connexion = mysql.connector.connect(
                host = "127.0.0.1",
                user = "root",
                password = "",
                database = "MYBASE"
                )
                for i in self.mytree.get_children():
                        self.mytree.delete(i)
                self.curseur = self.connexion.cursor()
                nom = self.entree_recherche.get()
                req = "select * from tache where name=%s"
                val=(nom,)
                self.curseur.execute(req,val)
                resultat=self.curseur.fetchall()
                if not resultat:
                        messagebox.showinfo("research",'task not found')
                else:
                        for row in resultat:
                        
                                self.mytree.insert('',index='end',values=(row[1],row[2],row[3],row[4],row[5]))
            except Exception as e:
                    messagebox.showerror("error",e)   
                    
# fonction permettant de terminer une tâche

    def termninate_task(self):
            try:
                resultat = self.selection_treeview()
                if  resultat =='':
                        messagebox.showerror('error','Select the task you want to finish')
                else:
                        
                        self.connexion = mysql.connector.connect(
                        host = "127.0.0.1",
                        user = "root",
                        password = "",
                        database = 'MYBASE'
                        )
                        self.curseur = self.connexion.cursor()  
                        req = 'UPDATE TACHE SET STATE = %s WHERE NAME = %s'
                        val = ("finish",resultat[0])
                        self.curseur.execute(req,val)
                        self.connexion.commit()
                        messagebox.showinfo('Task','Task successfuly finished')
                self.screen_all()
            except Exception as e:
                    messagebox.showerror('error',"An error occured when trying to finish the task.")
                        
                    
#cette fonction permettra la modification d'une tâche

    def modify_task(self):
            try:
                    resultat=self.selection_treeview()
                    if resultat == '' or resultat is None:
                            messagebox.showerror('Error','Please select a task to modify')
                    else:
                        self.entre_nom.delete(0,tk.END)
                        self.entre_nom.insert(0,resultat[0])
                        self.entre_date_debut.set_date(resultat[2])
                        self.entre_date_fin.set_date(resultat[3])
            except Exception as e:
                    messagebox.showerror('Error',str(e))
                    print(e)

#enregistrer une modification
    def save_modification(self):
            try:
                valeurs=self.recupere()
                resultat=self.selection_treeview()
                if valeurs==[]:
                        messagebox.showerror('error','fill task name or verify that dates are corrects')
                else:
                        if valeurs[2]>date.today():
                                req = 'UPDATE TACHE SET NAME=%s ,START_DATE=%s, DEADLINE=%s, PRIORITY=%s, STATE=%s WHERE NAME=%s'
                                val = (valeurs[0],valeurs[2],valeurs[3],valeurs[1], "waiting",resultat[0])
                                self.connexion = mysql.connector.connect(
                                        host = "127.0.0.1",
                                        user = "root",
                                        password = "",
                                        database = 'MYBASE'
                                        )
                                self.curseur = self.connexion.cursor() 
                                self.curseur.execute(req,val)
                                self.connexion.commit()  
                                self.entre_nom.delete(0,tk.END)
                                messagebox.showinfo("Task","Successfuly modify")
                                self.screen_all()
                        if valeurs[2]==date.today():
                                req = 'UPDATE TACHE SET NAME=%s ,START_DATE=%s, DEADLINE=%s, PRIORITY=%s, STATE=%s WHERE NAME=%s'
                                val = (valeurs[0],valeurs[2],valeurs[3],valeurs[1], "running",resultat[0])
                                self.connexion = mysql.connector.connect(
                                        host = "127.0.0.1",
                                        user = "root",
                                        password = "",
                                        database = 'MYBASE'
                                        )
                                self.curseur = self.connexion.cursor() 
                                self.curseur.execute(req,val)
                                self.connexion.commit()  
                                self.entre_nom.delete(0,tk.END)
                                messagebox.showinfo("Task","Successfuly modify")
                                self.screen_all()
                        if valeurs[3]<date.today():
                                messagebox.showerror("Error","You are trying to register a  late")
            except Exception as e:
                    messagebox.showerror('error','Modification failed')
                    print(e)
                    
#cette fonction permettra de mettre à jour l'état en retard 
    def update_state(self):
            try:
                    
                        self.connexion = mysql.connector.connect(
                        host = "127.0.0.1",
                        user = "root",
                        password = "",
                        database = 'MYBASE'
                        )
                        self.curseur = self.connexion.cursor()     
                        req1 ='UPDATE TACHE SET STATE=%s WHERE DEADLINE<CURDATE() AND STATE<>%s'
                        val1=("late", "finish")
                        self.curseur.execute(req1,val1)
                        self.connexion.commit()
                        req ='UPDATE TACHE SET STATE=%s WHERE START_DATE=CURDATE()'
                        val=("running", )
                        self.curseur.execute(req,val)
                        self.connexion.commit()
                        self.curseur.execute('SELECT * FROM TACHE WHERE STATE = %s',('late',))
                        resultats=self.curseur.fetchall()
                        if resultats:
                                messagebox.showinfo('Tasks',"You have late tasks")
                        
            except Exception as e:
                    messagebox.showerror('error',e)
                                        
        
