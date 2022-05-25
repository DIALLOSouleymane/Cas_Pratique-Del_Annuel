# -*- coding: utf-8 -*-
"""
Created on Fri May 20 14:52:41 2022

@authors:


    Souleymane DIALLO
    Ndeye Issa KA
    Tacko NDIAYE

    
"""



import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

# GUI
root = tk.Tk()

root.geometry("800x500") # dimensions
root.resizable(0, 0) #  root window fixe

#  TreeView Frame 
frame1 = tk.LabelFrame(root, text="Données Excel")
frame1.place(height=365, width=800)

# Ouverture du fichier
file_frame = tk.LabelFrame(root, text="Ouveture d'un fichier")
file_frame.place(height=100, width=400, rely=0.75, relx=0)

# Bouttons
b1 = tk.Button(file_frame, text="Charger un fichier", bg = "lightblue", fg = "black", command=lambda: Fichier_choix())
b1.place(rely=0.65, relx=0.72) 

b2 = tk.Button(file_frame, text="Afficher le fichier",bg = "lightblue", fg = "black", command=lambda: Charger())
b2.place(rely=0.65, relx=0.40)


# Fichier/ Chemin d'accès & Texte
label_file = ttk.Label(file_frame, text="Aucun fichier sélectionné")
label_file.place(rely=0, relx=0)


## Treeview Widget
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1) 

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) 
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) 
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) 
treescrollx.pack(side="bottom", fill="x") 
treescrolly.pack(side="right", fill="y") 


def Fichier_choix():
    """fonction pour charger le fichier via un chemin d'acces"""
    f = filedialog.askopenfilename(initialdir="/",
                                          title="Selectionner un fichier",
                                          filetype=(("fichier xlsx", "*.xlsx"),("Autres types", "*.*")))
    label_file["text"] = f
    return None


def Charger():
    """Si le fichier selectionné est valide, on charge le fichier sur l'objet Treeview"""
    fichier_path = label_file["text"]
    try:
        excel_filename = r"{}".format(fichier_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
        else:
            df = pd.read_excel(excel_filename)

    except ValueError:
        tk.messagebox.showerror("Information", "Le fichier sélectionné est invalide")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information",
                                f"Aucun fichier sélectionné, merci d'en sélectionner un et réessayer à nouveau...")
        return None

    Netoyer_treeview() # Suppression des anciennes donnees chargees sur treeview
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # column heading = nom colonne

    df_rows = df.to_numpy().tolist() # transformer le df en une matrice
    for row in df_rows:
        tv1.insert("", "end", values=row) # insertion de chaque liste sur le treeview. 
        #Details insertion https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None


def Netoyer_treeview():
    tv1.delete(*tv1.get_children())
    return None


root.mainloop()
