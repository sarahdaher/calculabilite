
#=====================================================#
# UE Calculabilite L3                                 #
# TME Automates a pile : acceptation d'un mot         #
# Mathieu.Jaume@lip6.fr                               #
#=====================================================#

from ensembles import *

#********************************************************************

# Automates a pile
# ================

# A = (st,alph,stack_alph,t_rel,init_st,init_stack,accept_mode,final_st,eq_st)
#
# st : etats
# alph : alphabet d'entree
# stack_alph : alphabet de la pile
# t_rel : relation de transtion
# init_st : etat initial
# init_stack : symbole de z dans la pile initiale
# accept_mode : 0 si pile vide, 1 si etat final
# final_st : liste d'etats finaux si accept_mode == 1, [] sinon
# eq_st : fonction d'egalite sur les etats
#

# Exemple
# -------

a1_st = ["q0","q1","q2"]
a1_alph = ["a","b","c"]
a1_stack_alph = ["z0"]
a1_t_rel = [(("q0","z0","a"),("q0",["z0","z0"])),\
            (("q0","z0",None),("q1",["z0"])),\
            (("q1","z0","b"),("q1",["z0"])),\
            (("q1","z0",None),("q2",[])),\
            (("q2","z0","c"),("q2",[]))]
a1_init_st = "q0"
a1_init_stack = "z0"
a1_accept_mode = 0
a1_final_st = []
a1_eq_st = eq_atom

a1_a = (a1_st,a1_alph,a1_stack_alph,a1_t_rel,a1_init_st,\
        a1_init_stack,a1_accept_mode,a1_final_st,a1_eq_st)

# Quelques fonctions de manipulation d'automates a pile
# -----------------------------------------------------


# Liste des parties droites de transitions avec x a partir de (q,s)

def find_trans(q,eq_st,t_rel,s,x):
    # q : etat
    # eq_st : fonction d'egalite sur les etats
    # t_rel : relation de transition
    # s : symbole de pile
    # x : etiquette (None ou symbole de l'alphabet)
    res = []
    for ((qr,zr,xr),(nqr,wr)) in t_rel:
        if xr==x and s==zr and eq_st(q,qr):
            res = res + [(nqr,wr)]
    return res

# Acceptation d'un mot par un automate a pile
# -------------------------------------------

# Liste des couples (configuration,mot) accessibles avec w
# a partir de la configuration c
# (les mots sont representes par des listes)

def next_configs(a,c,w):
    # a : automate a pile
    # c : configuration (etat,pile)
    # w : mot represente par une liste
    
    st,alph,stack_alph,t_rel,init_st,init_stack,accept_mode,final_st,eq_st = a
    q,s = c
    res =[]

    if s == []:
        return res
    
    transx = find_trans(q,eq_st,t_rel,s[0],None)
    for t in transx :
        nqr,sr = t
        res.append(((nqr,sr+s[1:]),w))

    if len(w) >0:
        transx = find_trans(q,eq_st,t_rel,s[0],w[0])
        for t in transx :
            nqr,sr = t
            res.append(((nqr,sr +s[1:]),w[1:]))

    return res 

def is_in_LA(a,w):
    # a : automate a pile
    # w : mot represente par une liste

    st,alph,stack_alph,t_rel,init_st,init_stack,accept_mode,final_st,eq_st = a

    configs = [((init_st,[init_stack]),w)]
    
    if configs == [] and w == "":
        if accept_mode == 1 :
            if is_in(eq_st,init_st,final_st) :
                return True
        
        if accept_mode == 0 :
            if init_stack ==[] :
                return True

    
    for config in configs :

        (etat,pile),mot = config
        

        if accept_mode == 1 :
            if mot=="" and is_in(eq_st,etat,final_st):
                return True
        
        if accept_mode == 0 :
            if mot=="" and pile ==[] :
                return True

        configs += next_configs(a,(etat,pile),mot)


    return False
