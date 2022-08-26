# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 18:18:01 2022

@author: lenovo
"""
from pulp import *
from contraintes import Contraintes



def pulp_optimize(budget=2000, sous_categ=['Oreo Biscuits Mini Chocolat', 'Anita Ail 50g - Anita', 'décoration']):
    
  # Définir les contraintes
  CT = Contraintes(budget, sous_categ)
  contraintes = CT.contraintes()
  #print(contraintes)
  choix = CT.choice_encode()
    
    
  # Initialiser les variables 
  variables = [LpVariable(i,lowBound=0, cat=LpInteger) for i in choix.keys()]
  #print(variables)
  
  # Initialiser le problème
  probleme = LpProblem(name='Répartition budget', sense=LpMaximize)
  
  
  # Ajouter contraintes budgéétaire
  contrainte_budget = LpConstraint(e=sum(variables), sense=LpConstraintLE, name='contrainte_budgétaire', rhs=budget)
  probleme.add(contrainte_budget)


  #palier = get_palier(df,budget)
  #contraintes = [float(df[df['Sous catégories dépenses']==elt][palier]) for elt in sous_categ]
  
  for elt in variables:
      
    contrainte = LpConstraint(e=elt, sense=LpConstraintGE, name='not null contrainte '+choix[elt.name], rhs=0)
    probleme.add(contrainte)
     
    contraintes_egalites = set().union(*(d.keys() for d in contraintes["egalites"]))  
    contraintes_inegalites = set().union(*(d.keys() for d in contraintes["inegalites"]))
    #print(contraintes_egalites)
    
    if choix[elt.name] in contraintes_inegalites:
        for sub in contraintes["inegalites"]:
            try:
                valeur = sub[choix[elt.name]]
            except:
                pass
         
        #probleme += (elt <= valeur)
        contrainte = LpConstraint(e=elt, sense=LpConstraintLE, name='contrainte '+choix[elt.name], rhs=valeur)
        probleme.add(contrainte)
          
    elif choix[elt.name] in contraintes_egalites:
        for sub in contraintes["egalites"]:
            try:
                valeur = sub[choix[elt.name]]
            except:
                pass
        #probleme += (elt == valeur)
        contrainte = LpConstraint(e=elt, sense=LpConstraintEQ, name='contrainte '+choix[elt.name], rhs=valeur)
        probleme.add(contrainte)


        
        
  # Ajouter la fonction objectif à maximiser au problème
  fonction_objectif = LpAffineExpression(e=sum(variables))
  probleme.setObjective(fonction_objectif)


  # Initialiser le solveur
  solver = PULP_CBC_CMD(timeLimit=20, msg=True)
  probleme.solve(solver=solver)
  
  
  # Afficher les résultats
  repartitions = {}
  for val in variables:
    #print(f"{val.name} = {choix[val.name]} : {val.value()}")
    repartitions[choix[val.name]] = str(round(val.value())) + " FCFA"
    

  return repartitions

