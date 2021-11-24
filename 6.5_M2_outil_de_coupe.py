from math import pi


def vitesseCoupe(diam, n):
    """ Retourne la vitesse de coupe VC (Vitesse linéaire de l'arête de coupe de l'outil) en m/s avec pour argument:
            diam : le diamètre de l'outil en mm
            n : la fréquence de rotation en tr/min """
    vc = pi * (diam / 10 ** 3) * (n / 60)
    print("La vitesse de coupe est de : ", round(vc, 2), ' m/s')
    return vc


def frequenceRotation(vc, diam):
    """ Retourne la fréquence de rotation en tr/min en fonction de la vitesse de coupe Vc avec pour argument:
            vc : vitesse de coupe en m/s
            diam : le diamètre de l'outil en mm """
    n = (vc * 60) / (pi * diam / 10 ** 3)
    print("La fréquence de rotation est de : ", round(n), ' tr/min')
    return n


def vitesseAvance(fz, n, z):
    """ Retourne la vitesse d'avance Vf en m/min avec pour argument:
            fz : vitesse d'avance par dent en mm (compris entre 0,8 mm pour la finition et 5 mm pour de l'ébauche)
            n : la fréquence de rotation en tr/min
            z : le nombre de dent """
    vf = (fz / 10 ** 3) * n * z
    print("La vitesse d'avance est de : ", round(vf, 2), ' m/min')
    return vf


def vitesseAvanceDent(vf, n, z):
    """ Retourne la vitesse d'avance par dent fz en mm avec pour argument:
            vf : vitesse d'avance en m/min 
            n : la fréquence de rotation en tr/min
            z : le nombre de dent """
    fz = (vf*10**3) / (n * z)
    print("La vitesse d'avance par dent est de : ", round(fz, 1), ' mm')
    return fz


if __name__ == '__main__':
    vitesseCoupe(140,6000)
    frequenceRotation(70,10)
    vitesseAvance(5, 3500, 4)
    vitesseAvanceDent(70, 3500, 4)
