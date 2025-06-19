import tkinter as tk
from tkinter import messagebox
import pandas as pd
import re

# Chargement du CSV
df = pd.read_csv("data/recettes.csv", sep=";")

# Fonction pour convertir les quantités en valeurs numériques
def convertir_quantite(qty):
    match = re.match(r"(\d+)", qty)
    if match:
        return int(match.group(1))
    return 0  # Retourne 0 si la quantité ne peut pas être convertie

# Fonction pour analyser les recettes
def recette_possible(ingredients_recette, quantites_recette, frigo):
    correspondants = 0
    manquants = {}
    for ing, qty in zip(ingredients_recette, quantites_recette):
        qty = convertir_quantite(qty)
        if ing in frigo and frigo[ing] >= qty:
            correspondants += 1
        else:
            manque = qty - frigo.get(ing, 0)
            manquants[ing] = manque
    taux = correspondants / len(ingredients_recette)
    return taux, manquants

# Fonction appelée par le bouton
def verifier_recettes():
    frigo_input = frigo_entry.get()
    if not frigo_input.strip():
        messagebox.showerror("Erreur", "Veuillez entrer les ingrédients du frigo.")
        return

    frigo_items = frigo_input.split(',')
    frigo = {}
    for item in frigo_items:
        try:
            nom, qty = item.split(':')
            frigo[nom.strip()] = int(qty)
        except ValueError:
            messagebox.showerror("Erreur", f"Format incorrect pour l'ingrédient : {item}")
            return

    result_box.delete('1.0', tk.END)

    for i, row in df.iterrows():
        ing_list = []
        qty_list = []
        for pair in row['Ingrédients'].split(','):
            try:
                nom, qte = pair.split(':')
                ing_list.append(nom.strip())
                qty_list.append(qte.strip())
            except ValueError:
                continue

        taux, manquants = recette_possible(ing_list, qty_list, frigo)
        if taux >= 0.0:
            result_box.insert(tk.END, f"✅ {row['Nom']} ({taux*100:.0f}%)\n")
            if manquants:
                result_box.insert(tk.END, f"   ❗ Ingrédients manquants : {manquants}\n\n")

# Interface graphique
root = tk.Tk()
root.title("Conseiller de Recettes")

tk.Label(root, text="Ingrédients du frigo (ex: Oeuf:2,Lait:500,Sel:1)").pack()
frigo_entry = tk.Entry(root, width=60)
frigo_entry.pack()

tk.Button(root, text="Vérifier les recettes", command=verifier_recettes).pack(pady=5)

result_box = tk.Text(root, height=20, width=80)
result_box.pack()

root.mainloop()