from part1 import *


def pion_adverse(n):
    assert n == 1 or n == 2, 'le joueur est différent de 1 et 2.'
    if n == 1:
        return 2
    return 1


def prise_possible_direction(plateau, i, j, vertical, horizontal, joueur):
    pion_adv = False
    while case_valide(plateau, i, j):  # si la case est valide
        i = i - vertical
        j = j + horizontal  # i, j de la case suivante
        if case_valide(plateau, i, j):  # si la case suivante est toujours valide
            if get_case(plateau, i, j) == pion_adverse(joueur):
                # la case suivante contient pion_adverse
                pion_adv = True
            else:
                # la case suivante ne contient pas pion_adverse
                return get_case(plateau, i, j) == joueur and pion_adv
                # True si c'est le joueur lui meme et on a trouve un pion adversaire dans cette direction
                # False si la case est libre ou on n'a pas trouve un pion adversaire
    return False


def mouvement_valide(plateau, i, j, joueur):
    # test pour tous les 8 directions
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
            # le pion est joueur lui meme, on arrete la fonction
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
                return True  # des qu'on trouve une case valide, return True
            j += 1
        i += 1
    return False  # la fonction a teste tous les cases possible mais il n'y a aucune cases valide


def fin_de_partie(plateau):
    return not(joueur_peut_jouer(plateau, 1) or joueur_peut_jouer(plateau, 2))


def gagnant(plateau):
    dico = {
        0: 0,
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


def test_pion_adverse():
    assert pion_adverse(1) == 2  # doit retourner True
    assert pion_adverse(2) == 1  # doit retourner True


def test_prise_possible_direction():
    p = creer_plateau(6)
    set_case(p, 0, 4, 2)
    set_case(p, 2, 2, 2)
    set_case(p, 4, 0, 2)
    set_case(p, 1, 4, 1)
    set_case(p, 2, 4, 1)
    set_case(p, 3, 3, 1)
    set_case(p, 3, 4, 1)
    set_case(p, 4, 1, 1)
    set_case(p, 4, 2, 1)
    set_case(p, 4, 3, 1)
    assert prise_possible_direction(p, 4, 4, 1, 0, 2)
    assert prise_possible_direction(p, 4, 4, 0, -1, 2)
    assert prise_possible_direction(p, 4, 4, 1, -1, 2)
    assert not prise_possible_direction(p, 4, 4, -1, 0, 2)
    assert not prise_possible_direction(p, 4, 4, -1, 1, 2)
    assert not prise_possible_direction(p, 4, 4, 1, 1, 2)


def test_mouvement_valide():
    p = creer_plateau(6)
    set_case(p, 0, 4, 2)
    set_case(p, 2, 2, 2)
    set_case(p, 4, 0, 2)
    set_case(p, 1, 4, 1)
    set_case(p, 2, 4, 1)
    set_case(p, 3, 3, 1)
    set_case(p, 3, 4, 1)
    set_case(p, 4, 1, 1)
    set_case(p, 4, 2, 1)
    set_case(p, 4, 3, 1)
    assert mouvement_valide(p, 4, 4, 2)
    assert not mouvement_valide(p, 4, 4, 1)
    assert mouvement_valide(p, 2, 1, 1)
    assert not mouvement_valide(p, 2, 1, 2)
    assert mouvement_valide(p, 2, 5, 2)
    assert not mouvement_valide(p, 2, 5, 1)


def test_mouvement_direction():
    p = creer_plateau(6)
    set_case(p, 0, 4, 2)
    set_case(p, 2, 2, 2)
    set_case(p, 4, 0, 2)
    set_case(p, 1, 4, 1)
    set_case(p, 2, 4, 1)
    set_case(p, 3, 3, 1)
    set_case(p, 3, 4, 1)
    set_case(p, 4, 1, 1)
    set_case(p, 4, 2, 1)
    set_case(p, 4, 3, 1)
    mouvement_direction(p, 4, 4, 1, 0, 2)
    assert get_case(p, 3, 4) == 2
    assert get_case(p, 2, 4) == 2
    assert get_case(p, 1, 4) == 2
    mouvement_direction(p, 4, 4, 0, -1, 2)
    assert get_case(p, 4, 3) == 2
    assert get_case(p, 4, 2) == 2
    assert get_case(p, 4, 1) == 2
    mouvement_direction(p, 4, 4, 1, -1, 2)
    assert get_case(p, 3, 3) == 2


def test_mouvement():
    p = creer_plateau(6)
    set_case(p, 0, 4, 2)
    set_case(p, 2, 2, 2)
    set_case(p, 4, 0, 2)
    set_case(p, 1, 4, 1)
    set_case(p, 2, 4, 1)
    set_case(p, 3, 3, 1)
    set_case(p, 3, 4, 1)
    set_case(p, 4, 1, 1)
    set_case(p, 4, 2, 1)
    set_case(p, 4, 3, 1)
    assert not get_case(p, 3, 4) == 2
    assert not get_case(p, 2, 4) == 2
    assert not get_case(p, 1, 4) == 2
    assert not get_case(p, 4, 3) == 2
    assert not get_case(p, 4, 2) == 2
    assert not get_case(p, 4, 1) == 2
    assert not get_case(p, 3, 3) == 2
    assert get_case(p, 5, 4) == 0
    assert get_case(p, 4, 5) == 0
    mouvement(p, 4, 4, 2)
    assert get_case(p, 3, 4) == 2
    assert get_case(p, 2, 4) == 2
    assert get_case(p, 1, 4) == 2
    assert get_case(p, 4, 3) == 2
    assert get_case(p, 4, 2) == 2
    assert get_case(p, 4, 1) == 2
    assert get_case(p, 3, 3) == 2
    assert get_case(p, 5, 4) == 0
    assert get_case(p, 4, 5) == 0


def test_joueur_peut_jouer():
    p = creer_plateau(4)
    assert joueur_peut_jouer(p, 1)  # retourne True
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p, 1, 1, 1)
    set_case(p, 2, 2, 1)
    assert not joueur_peut_jouer(p, 1)  # retourne False


def test_fin_de_partie():

    p = creer_plateau(4)
    assert not fin_de_partie(p) # retourne False
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p, 1, 1, 1)
    set_case(p, 2, 2, 1)
    assert fin_de_partie(p)  # retourne True


def test_gagnat():
    p = creer_plateau(4)
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p, 1, 1, 1)
    set_case(p, 2, 2, 1)
    assert gagnant(p) == 1  # retourne 1


if __name__ == '__main__':
    test_pion_adverse()
    test_mouvement_direction()
    test_mouvement_valide()
    test_mouvement()
    test_prise_possible_direction()
    test_gagnat()
    test_fin_de_partie()
    test_joueur_peut_jouer()
