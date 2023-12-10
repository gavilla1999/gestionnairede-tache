import tkinter as tk
#import fenetre1
#from fenetre1 import fenetre1
#def open():
#    fenetre1.mainloop()
    

fenetre2=tk.Tk()
fenetre2.title("TASKS MANAGER")
fenetre2.geometry("1000x800")
fenetre2.resizable(False,False)
fenetre2.configure(background="white")




bienvenue = tk.Label(fenetre2, text="Welcome on this tasks manager !!", background="skyblue", font=("Sans serif",20), relief='flat')
bienvenue.place(x=100, y=150, width=800, height=50)
bienvenue1 = tk.Label(fenetre2, text="On this app you can create and manage all your tasks easily\n So let us start !", background="skyblue", font=("Sans serif",15), relief='flat')
bienvenue1.place(x=200, y=210, width=600, height=80)
go_bouton = tk.Button(fenetre2, text="GO",bg="skyblue",command=open)
go_bouton.place(x=450, y=700, width=100)
if __name__=="__main__":
    fenetre2.mainloop()

    
    

