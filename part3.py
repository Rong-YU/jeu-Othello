from part2 import *
from json import dumps, loads
import os


def creer_partie(n):
    p = creer_plateau(n)
    partie = {"plateau": p,
              "joueur": 1}
    return partie


def saisie_valide(partie, s):
    if s == "m" or s == "y":
        return True
    s = s.lower()
    if len(s) == 2:
        if not("a" <= s[0] <= "z" and s[1].isdigit()):
            # la premiere caractere n'est pas une lettre ou la deuxieme n'est pas un chiffre
            # ou la chaine contient pas seulement deux caractere.
            return False
    else:
        return False
    i = ord(s[0])-97  # ex: a=0
    j = int(s[1])-1  # ex: 1=0
    if mouvement_valide(partie["plateau"], i, j, partie["joueur"]) == 0:
        print("Case non valide!")
        return False
    return True


def tour_jeu(partie):
    coord = joueur_peut_jouer(partie["plateau"], partie["joueur"])
    if coord == 0:
        print("joueur", partie["joueur"], "n'a pas de case disponible pour jouer")
        partie["joueur"] = pion_adverse(partie["joueur"])
        return True
    # os.system('clear')  # linux
    os.system('cls')  # pour Windows
    afficher_plateau_difficile(partie["plateau"])
    # afficher_plateau_simple(partie["plateau"])
    if partie["joueur"] == 1:
        print("C'est le tour du pion_blanc")
    else:
        print("C'est le tour du pion_noir")

    indice_max = 0
    i = 0
    while i < len(coord):
        if coord[i]["nb"] > coord[indice_max]["nb"]:
            indice_max = i
        i += 1
    coordonnes = coord[indice_max]["coord"]
    i = chr(coordonnes[0]+97)
    j = str(coordonnes[1]+1)
    print("sur la case", i + j, "vous pouvez manger", coord[indice_max]["nb"], "pions")

    s = ""
    print("saisir un mouvement(ex:B3),ou la lettre M pour accéder au menu principal ou Y pour accepter le conseil")
    while s == "" or not(saisie_valide(partie, s)):
        s = input()
        s = s.lower()
    if s == "m":
        return False
    if s == "y":
        i = coordonnes[0]
        j = coordonnes[1]
    else:
        i = ord(s[0])-97
        j = int(s[1])-1
    mouvement(partie["plateau"], i, j, partie["joueur"])
    partie["joueur"] = pion_adverse(partie["joueur"])
    return True


def saisir_action(partie=None):
    if partie is None: 
        print("saisir le numero d'action souhaite:")
        print("[0] terminer le jeu")
        print("[1] commencer une nouvelle partie")
        print("[2] charger une partie")
        s = input()
        while s not in ["0", "1", "2"]:
            s = input("Veuillez saisir seulement le numero.")
    else:
        print("saisir le numero d'action souhaite:")
        print("[0] terminer le jeu")
        print("[1] commencer une nouvelle partie")
        print("[2] charger une partie")
        print("[3] sauvegarder la partie en cours")
        print("[4] reprendre la partie en cours")
        s = input()
        while s not in ["0", "1", "2", "3", "4"]:
            s = input("Veuillez saisir seulement le numero.")
    return s


def jouer(partie):
    while not fin_de_partie(partie["plateau"]):
        if not tour_jeu(partie):
            return False


    # os.system('clear')  # linux
    os.system('cls')  # pour Windows
    afficher_plateau_difficile(partie["plateau"])
    # afficher_plateau_simple(partie["plateau"])

    return True


def saisir_taille_plateau():
    print("saisir la taille de plateau : 4, 6, 8")
    n = int(input())
    while n != 4 and n != 6 and n != 8:
        n = int(input())
    return n


def sauvegarder_partie(partie):
    partie = dumps(partie)
    f = open("sauvegarde_partie.json", "w")
    f.write(partie)
    f.close()


def charger_partie():
    if os.path.exists("sauvegarde_partie.json"):

        f = open("sauvegarde_partie.json", "r")
        partie = f.read()
        f.close()
        partie = loads(partie)
    else:
        print("pas de partie disponible, creer une nouvelle partie")
        n = saisir_taille_plateau()
        partie = creer_partie(n)
    return partie


def othello():
    action = saisir_action()
    if action == "0":
        return
    elif action == "1":
        n = saisir_taille_plateau()
        partie = creer_partie(n)
    elif action == "2":
        partie = charger_partie()

    while True:
        a = jouer(partie)
        if not a:
            action = saisir_action(partie)
            if action == "0":
                return
            elif action == "1":
                n = saisir_taille_plateau()
                partie = creer_partie(n)
                continue
            elif action == "2":
                partie = charger_partie()
                continue
            elif action == "3":
                sauvegarder_partie(partie)
                return
            elif action == 4:
                continue
        else:
            n = gagnant(partie["plateau"])
            if n == 1:
                print("joueur 1 a gagne")
            elif n == 2:
                print("joueur 2 a gagne")
            else:
                print("egalite")
            return
