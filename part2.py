from part1 import *


def pion_adverse(n):
    assert n == 1 or n == 2, 'le joueur est différent de 1 et 2.'
    if n == 1:
        return 2
    return 1


def prise_possible_direction(plateau, i, j, vertical, horizontal, joueur):
    if case_valide(plateau, i, j):  # si la case est valide
        if get_case(plateau, i, j) != 0:
            # la case n'est pas libre
            return False
        i = i - vertical
        j = j + horizontal  # coordonnee de la premiere case de direction donnee
        if case_valide(plateau, i, j):  # si la case est toujours valide
            if get_case(plateau, i, j) != pion_adverse(joueur):
                # premier case est joueur lui meme
                return False
    else:
        return False  # la case n'est pas valide
    while case_valide(plateau, i, j):  # si la case est valide
        if get_case(plateau, i, j) == pion_adverse(joueur):
            # la case suivante contient pion_adverse
            i = i - vertical
            j = j + horizontal  # coordonnee de la case suivante
        else:
            # la case suivante ne contient pas pion_adverse
            return get_case(plateau, i, j) == joueur # True si c'est le joueur lui meme, False si la case est libre
    return False


def mouvement_valide(plateau, i, j, joueur):
    return (
        prise_possible_direction(plateau, i, j, 0, -1, joueur) or
        prise_possible_direction(plateau, i, j, 1, -1, joueur) or
        prise_possible_direction(plateau, i, j, 1, 0, joueur) or
        prise_possible_direction(plateau, i, j, 1, 1, joueur) or
        prise_possible_direction(plateau, i, j, 0, 1, joueur) or
        prise_possible_direction(plateau, i, j, -1, 1, joueur) or
        prise_possible_direction(plateau, i, j, -1, 0, joueur) or
        prise_possible_direction(plateau, i, j, -1, -1, joueur)
    )


def mouvement_direction(plateau, i, j, vertical, horizontal, joueur):
    if not prise_possible_direction(plateau, i, j, vertical, horizontal, joueur):
        # cette direction n'est pas valide
        return
    i = i-vertical
    j = j+horizontal
    while case_valide(plateau, i, j):
        if get_case(plateau, i, j) == joueur:
            # rencontre lui meme
            return
        set_case(plateau, i, j, joueur)
        i = i-vertical
        j = j+horizontal


def mouvement(plateau, i, j, joueur):
    mouvement_direction(plateau, i, j, 0, -1, joueur)
    mouvement_direction(plateau, i, j, 1, -1, joueur)
    mouvement_direction(plateau, i, j, 1, 0, joueur)
    mouvement_direction(plateau, i, j, 1, 1, joueur)
    mouvement_direction(plateau, i, j, 0, 1, joueur)
    mouvement_direction(plateau, i, j, -1, 1, joueur)
    mouvement_direction(plateau, i, j, -1, 0, joueur)
    mouvement_direction(plateau, i, j, -1, -1, joueur)
    set_case(plateau, i, j, joueur)


def joueur_peut_jouer(plateau, joueur):
    n = plateau["n"]
    i = 0
    while i < n:
        j = 0
        while j < n:
            if mouvement_valide(plateau, i, j, joueur):
                # print("joueur",joueur,"peut jouer sur la case:",i,j)
                return True
            j += 1
        i += 1
    return False


def fin_de_partie(plateau):
    return not(joueur_peut_jouer(plateau, 1) or joueur_peut_jouer(plateau, 2))


def gagnant(plateau):
    dico = {
        1: 0,
        2: 0
    }
    i = 0
    while i < len(plateau["cases"]):
        dico[plateau["cases"][i]] += 1
        i += 1
    if dico[1] > dico[2]:
        return 1
    elif dico[2] > dico[1]:
        return 2
    else:
        return 0
