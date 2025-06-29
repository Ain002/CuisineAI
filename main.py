import tkinter as tk
from tkinter import messagebox
import pandas as pd
import re

# Chargement du CSV
df = pd.read_csv("data/recettes.csv", sep=";")

# convertion des quantités en valeurs numériques
def convertir_quantite(qt):
    match = re.match(r"(\d+)", qt)
    if match:
        return int(match.group(1))
    return 0  

# analyser des recettes
def recette_possible(ingredients_recette, quantites_recette, frigo):
    correspondants = 0
    manquants = {}
    for ing, qt in zip(ingredients_recette, quantites_recette):
        qt = convertir_quantite(qt)
        if ing in frigo and frigo[ing] >= qt:
            correspondants += 1
        else:
            manque = qt - frigo.get(ing, 0)
            manquants[ing] = manque
    taux = correspondants / len(ingredients_recette)
    return taux, manquants

# fonction appelée par le bouton
def verifier_recettes():
    frigo_input = frigo_entre.get()
    if not frigo_input.strip():
        messagebox.showerror("Erreur", "Veuillez entrer les ingrédients du frigo.")
        return

    frigo_items = frigo_input.split(',')
    frigo = {}
    for item in frigo_items:
        try:
            nom, qt = item.split(':')
            frigo[nom.strip().lower()] = int(qt)
        except ValueError:
            messagebox.showerror("Erreur", f"Format incorrect pour l'ingrédient : {item}")
            return

    result.delete('1.0', tk.END)

    for i, row in df.iterrows():
        ing_list = []
        qt_list = []
        for pair in row['Ingrédients'].split(','):
            try:
                nom, qte = pair.split(':')
                ing_list.append(nom.strip().lower())
                qt_list.append(qte.strip())
            except ValueError:
                continue

        taux, manquants = recette_possible(ing_list, qt_list, frigo)
        if taux >= 0.0:
            result.insert(tk.END, f"✅ {row['Nom']} ({taux*100:.0f}%)\n")
            if manquants:
                result.insert(tk.END, f"   ❗ Ingrédients manquants : {manquants}\n\n")

# Interface graphique
root = tk.Tk()
root.title("Conseiller de Recettes")

tk.Label(root, text="Ingrédients du frigo (ex: Oeuf:2,Lait:500,Sel:1)").pack()
frigo_entre = tk.Entry(root, width=60)
frigo_entre.pack()

tk.Button(root, text="Vérifier les recettes", command=verifier_recettes).pack(pady=5)

result = tk.Text(root, height=20, width=80)
result.pack()

root.mainloop()