from termcolor import *


def indice_valide(plateau, indice):
    return indice in range(0, plateau["n"])


def case_valide(plateau, i, j):
    return indice_valide(plateau, i) and indice_valide(plateau, j)


def get_case(plateau, i, j):
    assert case_valide(plateau, i, j), "la case n'est pas valide!"
    n = plateau["n"]
    indice = i * n + j
    return plateau["cases"][indice]


def set_case(plateau, i, j, val):
    assert case_valide(plateau, i, j), "la case n'est pas valide!"
    n = plateau["n"]
    indice = n * i + j
    plateau["cases"][indice] = val


def creer_plateau(n):
    assert n == 4 or n == 6 or n == 8, "La taille de plateau doit etre 4, 6, ou 8."
    tab = []
    i = 0
    while i < n * n:
        tab.append(0)
        i += 1
    centre= (n - 1) // 2
    indice = centre * n + centre
    tab[indice] = 2
    tab[indice + 1] = 1
    tab[indice + n] = 1
    tab[indice + n + 1] = 2
    dico = {"n": n, "cases": tab}
    return dico


def afficher_plateau_simple(plateau):
    n = plateau["n"]
    i = 0
    while i < n:
        c = ""
        j = 0
        while j < n:
            c += str(get_case(plateau, i, j))
            c += "  "
            j += 1
        print(c)
        i += 1


def afficher_plateau_moyen(plateau):
    n = plateau["n"]

    ligne = "*"
    i = 0
    while i < n:
        ligne += "********"
        i += 1

    point = "*"
    i = 0
    while i < n:
        point += "       *"
        i += 1

    i = 0
    print(ligne)
    while i < n:
        c = "*"
        j = 0
        while j < n:
            if get_case(plateau, i, j) == 1:
                c += "   N   *"
            elif get_case(plateau, i, j) == 2:
                c += "   B   *"
            else:
                c += "       *"
            j += 1
        print(point)
        print(c)
        print(point)
        print(ligne)
        i += 1


def afficher_plateau_difficile(plateau):
    n = plateau["n"]
    magenta = colored("       ", 'red', 'on_magenta')
    cyan = colored("       ", 'red', 'on_cyan')

    ligne_pair = "  "
    i = 0
    while i < n:
        if i % 2 == 0:
            ligne_pair += magenta
        else:
            ligne_pair += cyan
        i += 1

    ligne_impair = "  "
    i = 0
    while i < n:
        if i % 2 != 0:
            ligne_impair += magenta
        else:
            ligne_impair += cyan
        i += 1

    ligne_chiffre = "     "
    i = 0
    while i < n:
        ligne_chiffre += str(i+1)+"      "
        i += 1
    print(ligne_chiffre)

    i = 0
    while i < n:
        c = chr(97+i)+" "
        j = 0
        while j < n:
            pion = '###'
            couleur_pion = 'white'
            if get_case(plateau, i, j) == 1:
                couleur_pion = 'grey'
            elif get_case(plateau, i, j) == 0:
                pion = '   '
            if (i + j) % 2 == 0:
                c += colored("  ", 'red', 'on_magenta')+colored(pion, couleur_pion, 'on_magenta')+colored("  ", 'red','on_magenta')
            else:
                c += colored("  ", 'red', 'on_cyan')+colored(pion, couleur_pion, 'on_cyan')+colored("  ", 'red', 'on_cyan')
            j += 1
        if i % 2 == 0:
            print(ligne_pair)
            print(c)
            print(ligne_pair)
        else:
            print(ligne_impair)
            print(c)
            print(ligne_impair)
        i += 1


def test_indice_valide():
    p = creer_plateau(4)
    assert indice_valide(p, 0)  # doit retourner True car 0 est valide
    assert indice_valide(p, 3)  # doit retourner True car 3 est valide
    assert not indice_valide(p, -1)  # doit retourner False car -1 n'est pas valide
    assert not indice_valide(p, 4)  # doit retourner False car 4 n'est pas valide (si 4 cases : 0, 1, 2, 3)
    p = creer_plateau(6)
    assert indice_valide(p, 4)  # doit retourner True car on a maintenant 6 cases
    assert indice_valide(p, 5)  # doit retourner True car on a maintenant 6 cases
    assert not indice_valide(p, 6)  # doit retourner False  car les indices valides vont de 0 à 5
    print("indice_valide √")


def test_case_valide():
    p = creer_plateau(4)
    assert case_valide(p, 0, 0)
    assert not case_valide(p, -1, 0)
    assert not case_valide(p, 0, 5)
    print("case_valide √")


def test_get_case():
    p = creer_plateau(4)
    assert get_case(p, 0, 0) == 0
    assert not get_case(p, 0, 3) == 1
    # assert not get_case(p, 0, 4) == 0
    print("get_case √")


def test_set_case():
    p = creer_plateau(4)
    set_case(p, 0, 0, 3)
    assert get_case(p, 0, 0) == 3
    assert not get_case(p, 0, 3) == 1
    print("set_case √")


if __name__ == '__main__':
    test_indice_valide()
    test_case_valide()
    test_get_case()
    test_set_case()
