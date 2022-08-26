from data_processing import Datasets
import re
import unicodedata

nature, super_marche, produits_beautes = Datasets().read_data()

class Contraintes:
    
    def __init__(self, budget, choix):
        self.choix = choix
        self.budget = budget
        
    def get_palier(self):
        df = nature.copy()
        palier1 = list(df[df['Catégories dépenses']=="total dépenses cérémonies"]['Palier Prix 1'])[0]
        palier2 = list(df[df['Catégories dépenses']=="total dépenses cérémonies"]['Palier Prix 2'])[0]
        palier3 = list(df[df['Catégories dépenses']=="total dépenses cérémonies"]['Palier Prix 3'])[0]
        palier4 = list(df[df['Catégories dépenses']=="total dépenses cérémonies"]['Palier Prix 4'])[0]
        #print(f"Budget : {self.budget}\nPalier 1 : {palier1}")
        
        palier = (self.budget <= float(palier1) and "Palier Prix 1") or (self.budget <= float(palier2) and "Palier Prix 2") or (self.budget <= float(palier3) and "Palier Prix 3") or "Palier Prix 4"
        return palier
    
    # Supprimer les accents et les espaces
    def choice_encode(self):
        vals = {}
        for i in range(len(self.choix)):
            vals["X"+str(i+1)] = self.choix[i]
        return vals
        
    def contraintes(self):
        palier = self.get_palier()
        contraintes = {"egalites": [], "inegalites": []}
        self.choix = [elt.lower().strip() for elt in self.choix]
        for elt in self.choix:
            if(elt in list(nature['Sous catégories dépenses'].str.lower())):
                prix = float(nature[nature['Sous catégories dépenses'] == elt][palier])
                contraintes["inegalites"].append({elt: prix})
                
            elif(elt in list(super_marche["Produit"].str.lower())):
                prix = float(super_marche[super_marche["Produit"] == elt]["Prix"])
                contraintes["egalites"].append({elt: prix})
                
            elif(elt in list(produits_beautes["Product"].str.lower())):
                prix = float(produits_beautes[produits_beautes["Product"] == elt]["Price"])
                contraintes["egalites"].append({elt: prix})
                
            else:
                pass
                
        return contraintes