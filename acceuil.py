import tkinter as tk
import g_tache1 as gt
def open():
    root = tk.Tk()
    global fenetreT 
    fenetreT =gt.Tache(root)
    fenetreT.update_state()
    root.mainloop()


fenetre2=tk.Tk()
fenetre2.title("TASKS MANAGER")
fenetre2.geometry("1800x800")
fenetre2.resizable(False,False)
fenetre2.configure(background="white")
bienvenue = tk.Label(fenetre2, text="Welcome on this tasks manager !!", background="skyblue", font=("Sans serif",20), relief='flat')
bienvenue.place(x=300, y=150, width=1000, height=50)
bienvenue1 = tk.Label(fenetre2, text="On this app you can create and manage all your tasks easily\n So let us start !", background="skyblue", font=("Sans serif",15), relief='flat')
bienvenue1.place(x=500, y=210, width=600, height=80)
go_bouton = tk.Button(fenetre2, text="GO",bg="skyblue",command=open)
go_bouton.place(x=700, y=700, width=100)
fenetre2.mainloop()
        

if __name__=="__main__":
   fenetre2.mainloop()
   
    
    

