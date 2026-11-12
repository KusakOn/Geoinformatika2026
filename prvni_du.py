# Na vstupu budou seznamy X,Y,Z

import statistics as stat
import numpy as np


def vzdalenost_bodu (prvni, druhy, X, Y, Z):
    prvni_souradnice = (X[prvni] - X[druhy])**2
    druha_souradnice = (Y[prvni] - Y[druhy])**2
    treti_souradnice = (Z[prvni] - Z[druhy])**2
    return (prvni_souradnice + druha_souradnice + treti_souradnice)**(1/2)


def nejblizsi_sousedi_naivne (bod, X, Y, Z, pocet_sousedu):          # spatial density of cloud
    
    seznam_blizkych = {}
    hranice = False

    for x in range (len(X)):
        if x != bod:
            vzdalenost = vzdalenost_bodu(bod, x, X, Y, Z)

            if (len(seznam_blizkych) < pocet_sousedu):      # Zatim mame malo sousedu
                seznam_blizkych[x] = vzdalenost
                if (hranice == False or vzdalenost > hranice):
                    hranice = vzdalenost

            elif (hranice > vzdalenost):                     # Vylepseni sousedu
                seznam_blizkych[x] = vzdalenost

                for y in seznam_blizkych:
                    if seznam_blizkych[y] == hranice:
                        seznam_blizkych.pop(y)
                        break

                nova_hranice = 0
                for y in seznam_blizkych:
                    if (seznam_blizkych[y] > nova_hranice):
                        nova_hranice = seznam_blizkych[y]

                hranice = nova_hranice


    return seznam_blizkych


def spocitej_krivost (X,Y,Z):                         # Spacial curvature
    hodnoty = []
    for cislo in range(len(X)):


        hodnoty.append()
    return hodnoty


def prostorova_hustota (X,Y,Z, metoda = "N"):

    velikost_mracna = len(X)

    soucet = 0

    if metoda == "N":
        for cislo in range(len(X)):
            nejblizsi_bod = nejblizsi_sousedi_naivne(cislo, X,Y,Z, 1) [0]
            soucet += vzdalenost_bodu(cislo, nejblizsi_bod, X, Y, Z)

    if metoda == "V":
        for cislo in  range(len(X)):
            nejblizsi_bod = 
            soucet += vzdalenost_bodu(cislo, nejblizsi_bod, X, Y, Z)

    if metoda == "":

    prumer = soucet / velikost_mracna

    return 1 / prumer**(1/3)


# https://www.emergentmind.com/topics/local-point-cloud-curvature

# https://www.algosome.com/articles/pca-three-dimensions-point-cloud.html

# https://en.wikipedia.org/wiki/Principal_component_analysis

# https://en.wikipedia.org/wiki/Covariance_matrix



def kovariacni_matice (bod, sousedi):

    prvni_souradnice = [X[soused]]
    druha_souradnice = [Y[soused]]
    treti_souradnice = [Z[soused]]

    for soused in sousedi:    
        prvni_souradnice.append( X[soused])
        druha_souradnice.append( Y[soused])
        treti_souradnice.append( Z[soused])

    a_11 = stat.pvariance(prvni_souradnice)
    a_22 = stat.pvariance(druha_souradnice)
    a_33 = stat.pvariance(treti_souradnice)
    a_12 = stat.covariance(prvni_souradnice,druha_souradnice)
    a_13 = stat.covariance(prvni_souradnice, treti_souradnice)                   #pvariance   vs variance
    a_23 = stat.covariance(druha_souradnice, treti_souradnice)

    M = np.array( [ [a_11, a_12, a_13],[a_12,a_22, a_23] [a_13,a_23,a_33] ] )          # Variancne kovariancni matice

    vl_cisla, vl_vektory = np.linalg.eig(M)                                       # Vlastni cisla realna

    vl_cisla.sort()

    alfa_1 = vl_cisla[0]
    alfa_2 = vl_cisla[1]
    alfa_3 = vl_cisla[2]

    return alfa_1 / (alfa_1 + alfa_2 + alfa_3)                 # Nemuzu delit nulou?


def krivost (X,Y,Z, metoda = "A"):

    reseni = []

    if metoda == "A":
        for x in range(len(X)):
            reseni.append(kovariacni_matice (x, ))
            
    else:
        for x in range (len(X)):
            reseni.append(kovariacni_matice(x, ))

    return reseni

class KDNode:

    def __init__(self, point=None, axis=None, left=None, right=None, point_indices=None):
    
        self.point = point
        self.axis = axis
        self.left = left
        self.right = right
        self.point_indices = point_indices
        
        
class KDTree:

    def __init__(self, data, X, Y, Z):
        
        self.data = array(data)  # Ensure data is a NumPy array
        self.root = None

        
    def _build_tree(self, idxs, depth):
        hloubka = 0

        self.root = KDNode()
        resene = {self.root : self.data}              #Slovnik, vrchol a body v nem dosazitelne
        dalsi_kolo = {}          # Pro dalsi kolo.

        

        while hloubka != 10:
            d = hloubka % 3

            for vrchol in resene:

                seznam = resene[vrchol]

                if d == 0:

                    souradnice = []
                    for x in seznam:
                        souradnice.append(self.X[x])
                    x_m = median_hrube(souradnice)

                elif d == 1:

                    souradnice = []
                    for y in seznam:
                        souradnice.append(self.Y[y])

                    y_m = median_hrube(souradnice)
            
                else:
                    souradnice = []
                    for z in seznam:
                        souradnice.append(self.Z[z])

                    z_m = median_hrube(souradnice)



            hloubka += 1




def median_hrube(seznam):
    seznam.sort()
    n = len(seznam)
    if (n % 2 == 0):
        return (seznam[n/2] + seznam[n/2 - 1])/2
    else:
        return seznam[int (n/2)]


def median_usporadaneho_seznamu (seznam):
    n = len(seznam)
    if (n % 2 == 0):
        return (seznam[n/2] + seznam[n/2 - 1])/2
    else:
        return seznam[int (n/2)]











def normalizuj_souradnice(bod, seznam_extremu = None, X = None, Y=None, Z = None):

    if seznam_extremu == None:

        x_i = (X[bod] - min(X)) / (max(X) - min (X))
        y_i = (Y[bod] - min(Y)) / (max(Y) - min (Y))
        z_i = (Z[bod] - min(Z)) / (max(Z) - min (Z))

    else:

        x_i = (X[bod] - seznam_extremu[0])/(seznam_extremu[1] - seznam_extremu[0])
        y_i = (Y[bod] - seznam_extremu[2])/(seznam_extremu[3] - seznam_extremu[2])
        z_i = (Z[bod] - seznam_extremu[4])/(seznam_extremu[5] - seznam_extremu[4])

    return [x_i, y_i, z_i]



def hash_bunky(jx, jy, jz, nr):
    return jx +jy * nr + jz*nr*nr


def nadrazena_bunka (relativni_souradnice, n_r):
    c = 0.99
    ix = int( c *  n_r * relativni_souradnice[0] )
    iy = int( c *  n_r * relativni_souradnice[1] )
    iz = int( c *  n_r * relativni_souradnice[2] )
    return [ix, iy, iz]



def vytvor_H_J (X,Y,Z):

    n = len(X)
    n_r = n ** (1/9)
    J = []
    H = { x: [] for x in range (n_r**3 -1)}
    n_r = n ** (1/9)

    X_max = max(X)
    Y_max = max(Y)
    Z_max = max(Z)

    X_min = min(X)
    Y_min = min(Y)
    Z_min = min(Z)

    extremy = [X_min, X_max, Y_min, Y_max, Z_min, Z_max]

    for bod in range (len(X)):

        relativni = normalizuj_souradnice(bod, extremy)
        bunka = nadrazena_bunka(relativni, n_r)
        v_1D = hash_bunky(bunka[0], bunka[1], bunka[2], n_r)

        J.append(v_1D)
        H[v_1D].append(bod)


    return J, H


def nejblize (bod, H,J, pocet_sousedu, X,Y,Z):     #alespon 2 iterace navic

    kandidati = set (H(J [bod]))   # vsichni spolubunkovci

    kandidati.remove(bod)

    pokus = 1

    while len(kandidati) < pocet_sousedu :            #Predpoklad vice bodu nez sousedu
        kandidati.update(sousedstvi (bod, pokus, !!!!!!!!  ))
        pokus += 1

    kandidati.update(sousedstvi (bod, pokus,  ))

    kandidati.update(sousedstvi (bod, pokus + 1, !!!!!!!!!  ))

    return  nejblizsi_sousedi_s_omezenim (bod, X, Y, Z, pocet_sousedu, kandidati)   # jina funkce, iterujeme pres povolene










def sousedstvi (bunka, o_kolik, hrana_krychle):

    validni = set ()

    for prvni_osa in range (- o_kolik, o_kolik):
        for druha_osa in range( - (o_kolik - abs(prvni_osa)), (o_kolik - abs(prvni_osa))):
            
            treti_osa = - (o_kolik - abs(prvni_osa) - abs(druha_osa))

            if (bunka%hrana_krychle + prvni_osa in range (hrana_krychle -1,0) and ):
                cil = bunka + prvni_osa +druha_osa * hrana_krychle + treti_osa * hrana_krychle * hrana_krychle
                
                validni.add(cil)

            treti_osa = o_kolik - abs(prvni_osa) - abs(druha_osa)


            if ():
                cil = bunka + prvni_osa +druha_osa * hrana_krychle + treti_osa * hrana_krychle * hrana_krychle
                validni.add(cil)


    return validni

















def nejblizsi_sousedi_s_omezenim (bod, X, Y, Z, pocet_sousedu, omezeni):          # spatial density of cloud
    
    seznam_blizkych = {}
    hranice = False

    for x in omezeni:
        if x != bod:
            vzdalenost = vzdalenost_bodu(bod, x, X, Y, Z)

            if (len(seznam_blizkych) < pocet_sousedu):      # Zatim mame malo sousedu
                seznam_blizkych[x] = vzdalenost
                if (hranice == False or vzdalenost > hranice):
                    hranice = vzdalenost

            elif (hranice > vzdalenost):                     # Vylepseni sousedu
                seznam_blizkych[x] = vzdalenost

                for y in seznam_blizkych:
                    if seznam_blizkych[y] == hranice:
                        seznam_blizkych.pop(y)
                        break

                nova_hranice = 0
                for y in seznam_blizkych:
                    if (seznam_blizkych[y] > nova_hranice):
                        nova_hranice = seznam_blizkych[y]

                hranice = nova_hranice


    return seznam_blizkych








class OCstrom:

    def __init__(self, data, koren):
        self.body = data



    def sestav_strom (X,Y,Z):



class vrchol_Ocstromu:

    def __init__(self, oznaceni, body = None, deti = None):

        self.deti = deti
        self.oznaceni = oznaceni
        self.body = body


    def vypln_vrchol ()