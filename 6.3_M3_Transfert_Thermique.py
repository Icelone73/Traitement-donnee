from math import *


def resistTherm(lam, ep, cp="parois", r0=0.0):
    """ Retourne la résistance thermique R d'un matériaux en W/m²*K avec pour argument :
            l : Coéfficient thermique (lambda) en W/m*k
            ep : Epaisseur du matériaux en mm
            r0 : dans le cas d'une conduite distance depuis le centre de la conduite jusqu'à la parois considéré
                 du tuyaux en mm """
    if cp == 'Conduite' or cp == 'conduite':
        r = log((ep + r0) / r0) / (2 * pi * lam)
    else:
        r = (ep / 10 ** 3) / lam
    return r


def resistThermTot():
    """ Retourne la résistance thermique R d'un complexe de parois ou de conduit en W/m²*K grace à la fonction
    'resistTherm' tant que l'utilisateur ne presse pas entrer vide """
    rt = 0
    cp = input("Conduite ou Parois ? ")
    while 1:
        name = input('Entrer le nom du matériau (ou <entrer> pour quitter) : ')
        if name == "":
            break
        else:
            if cp == 'Conduite' or cp == 'conduite':
                ri = float(input("Entrer la distance depuis le centre du conduit "
                                 "jusqu'à la parois traité en mm (R0): "))
            else:
                ri = 0.0
            ep = float(input("Entrer l'épaisseur du matériau en mm : "))
            lam = float(input('Entrer le lambda du matériau en W/m*K : '))
            r = resistTherm(lam, ep, cp, ri)
            rt = rt + r
            resist = "Le matériau {} à une résistance thermique de {:6.6f} m²*K/W "
            print(resist.format(name, r))
    print("la résistance thermique totale est de : ", round(rt, 6), "m²*K/W")
    return rt


def flux_Chaleur(ti, te):
    """ Retourne le flux de chaleur à travers une parois (conduction) en W/m² ou W/m avec pour argument :
            ti : Température intérieur en °C
            te : Température extérieur en °C """
    phi = (ti - te) / resistThermTot()
    print("Le flux de chaleur à travers la parois est de : ", round(phi, 3), "W/m² pour une parois et "
                                                                             "W/m pour une conduite")
    return phi


def coefhForcer(p, v, d, lam, cp, mu, mup=0.0, lo=0.0):
    """ Défini le coefficient de transfert h pour le calcul du flux par convection forcée avec pour argument:
            p : Masse volumique du fluide en kg/m3
            v : La vitesse du fluide en m/s
            d : Le diamètre intérieur de la conduite en mm (Attention Dh pour conduite non circulaire !)
            lam : Conductivité thermique du fluide en W/m*K
            cp : Pouvoir calorifique du fluide en J/kg*K
            mu : Viscosité du fluide en Pa.s
            mup : Viscosité du fluide à la parois en Pa.s
            lo : Longueur de la conduite en m"""
    d = d / 10 ** 3
    pr = (cp * mu) / lam
    re = (p * v * d) / mu
    print("Pr = ", round(pr, 3))
    print("Re = ", round(re))
    if re < 2100:
        nu = 1.86 * ((d / lo) * pr * re) ** (1 / 3) * (mu / mup) ** 0.14
        print("Re < 2100 donc régime laminaire ! Nu = ", round(nu, 2))
    elif 2100 < re < 10000:
        nu = 0.116 * (re ** (2 / 3) - 125) * pr ** (1 / 3) * (1 + (d / lo) ** (2 / 3)) * (mu / mup) ** 0.14
        print("2100 < Re < 10000 donc régime intermédiaire ! Nu = ", round(nu, 2))
    else:
        nu = 0.023 * re ** 0.8 * pr ** (1 / 3)
        print("Re > 10000 donc régime turbulent ! Nu = ", round(nu, 2))
    h = nu * lam / d
    print("Le coefficient de tranfert est de : ", round(h, 3), " W/m²*K")
    return h


def coefhNaturel(p, g, d, dt, lam, cp, beta, mu):
    """ Défini le coefficient de transfert h pour le calcul du flux par convection naturelle avec pour argument:
                p : Masse volumique du fluide en kg/m3
                g : Accélération de pesanteur en m/s²
                d : Longueur caractéristique de l'échange en mm (Attention Dh pour conduite non circulaire
                    dans le cas 4 !)
                dt : Delta de température en K
                lam : Conductivité thermique du fluide en W/m*K
                cp : Pouvoir calorifique du fluide en J/kg*K
                beta : Coefficient d'expension thermique du fluide en K-1
                mu : Viscosité du fluide en Pa.s"""
    print("1 : Parois vertical d = hauteur")
    print("2 : Parois horizontale type plancher d = longueur")
    print("3 : Parois horizontale type toiture d = longueur")
    print("4 : Cylindre horizontal d = diamètre conduite")
    print("5 : Cylindre vertical d = hauteur")
    cat = input("Quelle est le type de transfert ? ")

    nu = 0
    d = d / 10 ** 3
    pr = (cp * mu) / lam
    gr = (dt * beta * d ** 3 * p ** 2 * g) / mu ** 2
    ecoulement = gr * pr
    print("Pr = ", round(pr, 3))
    print("Gr = ", round(gr, 3))
    print("Gr x Pr = ", round(ecoulement))

    if 10 ** 4 < ecoulement < 10 ** 9:
        if cat == "1" or cat == "5":
            nu = 0.55 * ecoulement ** 0.25
        elif cat == "2":
            nu = 0.54 * ecoulement ** 0.25
        elif cat == "3":
            nu = 0.27 * ecoulement ** 0.25
        else:
            nu = 0.53 * ecoulement ** 0.25
        print("10^4 < Gr x Pr < 10^9 donc régime laminaire ! Nu = ", round(nu, 2))

    elif ecoulement > 10 ** 9:
        if cat == "2" or cat == "4" or cat == "5":
            nu = 0.14 * ecoulement ** 0.33
        elif cat == "1":
            nu = 0.13 * ecoulement ** 0.33
        else:
            print("Impossible de calculer car pas d'équation pour type 3 en turbulent ")
        print("Gr x Pr > 10^9 donc régime turbulent ! Nu = ", round(nu, 2))

    else:
        print("infaisable car 10^4 < Gr x Pr")
    h = nu * lam / d
    print("Le coefficient de tranfert est de : ", round(h, 3), " W/m²*K")
    return h


def flux_Chaleur_Convec(ti, te):
    """ Retourne le flux de chaleur du à la convection en W/m² avec pour argument :
            ti : Température intérieur en °C
            te : Température extérieur en °C """
    nature = input("Convection Forcer ou Naturelle ? ")
    p = int(input("Densité du fluide en kg/m3 : "))
    lam = float(input("Conductivité thermique du fluide en W/m*K : "))
    cp = float(input("Pouvoir calorifique du fluide en J/kg*K : "))
    mu = eval(input("Viscosité du fluide en Pa/s : "))

    if nature == "Naturelle" or nature == "naturelle" or nature == "Naturel" or nature == "naturel":
        dt = ti - te
        g = float(input("Accélération de pesanteur en m/s² : "))
        d = float(input("Longueur caractéristique de l'échange en mm (Attention Dh pour conduite non circulaire dans "
                        "le cas 4 !) : "))
        beta = eval(input("Coefficient d'expension thermique du fluide en K-1 : "))
        h = coefhNaturel(p, g, d, dt, lam, cp, beta, mu)
    else:
        v = float(input("La vitesse du fluide en m/s : "))
        d = float(input("Le diamètre intérieur de la conduite en mm (Attention Dh pour conduite non circulaire !) : "))
        mup = eval(input("Viscosité du fluide à la parois en Pa/s : "))
        lo = float(input("Longueur de la conduite en m : "))
        h = coefhForcer(p, v, d, lam, cp, mu, mup, lo)
    phi = (ti - te) * h
    print("Le flux de chaleur en convection est de : ", round(phi, 3), "W/m²")
    return phi



