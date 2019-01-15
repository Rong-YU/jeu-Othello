from part2 import *
from json import dumps, loads
import os


def creer_partie(n):
    p = creer_plateau(n)
    partie = {"plateau": p,
              "joueur": 1}
    return partie


def saisie_valide(partie, s):
    s = s.lower()
    if s == "m" or s == "y":
        return True
    if len(s) == 2:  # si la chaine contient seulement deux caractere.
        if not("a" <= s[0] <= "z" and s[1].isdigit()):
            # la premiere caractere n'est pas une lettre ou la deuxieme n'est pas un chiffre
            return False
    else:
        return False
    i = ord(s[0])-97  # ex: a=0
    j = int(s[1])-1  # ex: 1=0
    if mouvement_valide(partie["plateau"], i, j, partie["joueur"]) == 0:  # verifier si le mouvement est valide
        print("Case non valide!")
        return False
    return True


def tour_jeu(partie):
    coord = joueur_peut_jouer(partie["plateau"], partie["joueur"])  # les coordonnees de mouvement valide
    if coord == 0:  # si y a pas de mouvement valide
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

    indice_max = 0  # trouver la case ou le joueur peut manger le plus de pion
    i = 0
    while i < len(coord):
        if coord[i]["nb"] > coord[indice_max]["nb"]:
            indice_max = i
        i += 1
    coordonnes = coord[indice_max]["coord"]   # les coordonnes de la case ou on peut manger le plus de pion
    i = chr(coordonnes[0]+97).upper()
    j = str(coordonnes[1]+1)
    print("sur la case", i + j, "vous pouvez manger", coord[indice_max]["nb"], "pions")

    s = ""
    print("saisir un mouvement(ex:B3),ou la lettre M pour accéder au menu principal ou Y pour accepter le conseil")
    while s == "" or not(saisie_valide(partie, s)):
        s = input()
    s = s.lower()  # pour faciliter la calcule ASCII d'apres
    if s == "m":
        return False
    if s == "y":  # si le joueur accepter le conseil
        i = coordonnes[0]
        j = coordonnes[1]
    else:  # si le joueur a choisi une case par luimeme
        i = ord(s[0])-97
        j = int(s[1])-1
    mouvement(partie["plateau"], i, j, partie["joueur"])  # effectuer le mouvement
    partie["joueur"] = pion_adverse(partie["joueur"])  # changer le joueur pour le tour suivant
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
    while not fin_de_partie(partie["plateau"]):  # tant que la partie n'est pas terminee
        if not tour_jeu(partie):  # appel la fonction tour_jeu
            # la fonction renvoi false seulement le joueur courant souhaite retourner au menu principal
            return False
        # si non le mouvement doit etre effectue, et fait rien.

    # la partie est terminee, afficher la plateau
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
        if not jouer(partie):
            # False = la partie s'est terminée car l'un des joueurs a souhaité accéder au menu principal
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
        else:  # True = la partie est finalement terminée
            n = gagnant(partie["plateau"])
            if n == 1:
                print("joueur 1 a gagne")
            elif n == 2:
                print("joueur 2 a gagne")
            else:
                print("egalite")
            return


def test_creer_partie():
    p = creer_partie(4)
    plateau = creer_plateau(4)
    assert p == {"plateau": plateau, "joueur": 1}
    p = creer_partie(6)
    plateau = creer_plateau(6)
    assert p == {"plateau": plateau, "joueur": 1}
    p = creer_partie(8)
    plateau = creer_plateau(8)
    assert p == {"plateau": plateau, "joueur": 1}


def test_saisie_valide():
    p = creer_partie(4)
    s = "m"
    assert saisie_valide(p, s)
    s = "M"
    assert saisie_valide(p, s)
    s = "y"
    assert saisie_valide(p, s)
    s = "Y"
    assert saisie_valide(p, s)
    s = "b1"
    assert saisie_valide(p, s)
    s = "E1"
    assert not saisie_valide(p, s)


def test_charger_partie():
    partie = creer_partie(4)
    sauvegarder_partie(partie)
    partie1 = charger_partie()
    assert partie == partie1
    os.remove("sauvegarde_partie.json")


def test_sauvegarder_partie():
    partie = creer_partie(4)
    assert not os.path.exists("sauvegarde_partie.json")
    sauvegarder_partie(partie)
    assert os.path.exists("sauvegarde_partie.json")
    os.remove("sauvegarde_partie.json")


if __name__ == '__main__':
    test_saisie_valide()
    test_creer_partie()
    test_charger_partie()
    test_sauvegarder_partie()
