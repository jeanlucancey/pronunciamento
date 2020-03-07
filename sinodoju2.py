#! /usr/bin/env python3
# coding: utf8

# IMPORTANT - Ce listing fait partie du projet Django tout
# en n'en faisant pas partie... Il n'est pas lancé par Django
# lui-même mais par une commande "system" dans un fichier "views.py"
# (de l'application "dialogue" au moment où j'écris ces lignes).
# Non, ce n'est pas n'importe quoi: c'est parce que cette bidouille
# est vouée à être également lancée sur d'autres serveurs, et cette
# fois par des scripts PHP... sans Django, donc. Pour permettre une
# homogénéité de traitement entre mon serveur Django chez AlwaysData
# et mes serveurs PHP chez Phpnet et Alphosting-Tizoo, j'utilise à
# peu près le même listing dans les trois cas (il y a des variantes
# subtiles). Mais du coup c'est mon Django qui n'est plus totalement
# homogène... Tant pis. Je suis un adepte des bricolages quick and
# dirty et je vous emmerde. :-P

import time
import sys
from os import system
import http.client
from urllib.parse import urlencode, quote_plus
import base64


# --- Definitions de classes

class Fichier:
    def __init__(self, nomFichierArg, boolEcriture):
        self.nomFichier = nomFichierArg
        if boolEcriture:
            self.fichier = open(self.nomFichier, 'wb') # 'b' pour des octets
            self.fichier.seek(0, 0) # Se place au debut du fichier
            self.longueur = 0
        else:
            self.fichier = open(self.nomFichier, 'rb') # 'b' pour des octets
            self.fichier.seek(0, 2) # Se place a la fin du fichier
            self.longueur = self.fichier.tell()
        self.index = 0

    def close (self):
        self.fichier.close()

    def deByteStringAChaineUnicode (self, monByteString):
        chaineUnicode = monByteString.decode(encoding='UTF-8')
        return chaineUnicode

    def deChaineUnicodeAByteString (self, chaineUnicode):
        monByteString = chaineUnicode.encode(encoding='UTF-8')
        return monByteString

    def ecritUneLigne (self, ligneAEcrire):
        ligneAEcrire2 = self.deChaineUnicodeAByteString(ligneAEcrire)
        for numOctet in range(len(ligneAEcrire2)):
            octet = ligneAEcrire2[numOctet:numOctet + 1]
            # La ligne precedente a l'air amphigourique, mais
            # ligneAEcrire2[numOctet:numOctet + 1] est de type "bytes",
            # alors que ligneAEcrire2[numOctet] serait de type "int"
            self.ecritUnOctet(octet)
        self.ecritUnOctet(b'\n')

    def ecritUnOctet (self, signe):
        self.fichier.seek(self.index, 0)
        self.fichier.write(signe)
        self.index += 1
        self.longueur += 1

    def interromptLecture (self):
        self.close()

    def litUneLigne (self):
        octetLu = ''
        ligneLue = b"" # Soit un bytestring vide
        finDeLigne = 0 # false

        while self.index < self.longueur and not finDeLigne:
            octetLu = self.litUnOctet(self.index)
            if octetLu == b'\n':
                finDeLigne = 1 # true
            else:
                ligneLue += octetLu

        ligneLue2 = self.deByteStringAChaineUnicode(ligneLue)
        return ligneLue2

    def litUnOctet (self, numOctet):
        self.fichier.seek(numOctet, 0)
        octet = self.fichier.read(1)
        self.index += 1
        return octet

    def reprendLecture (self):
        self.fichier = open(self.nomFichier, 'r')
        self.fichier.seek(self.index, 0) # Se place ou on s'etait arrete

    def seek (self, numOctet):
        self.fichier.seek(numOctet, 0)
        self.index = numOctet


# --- Definitions de fonctions

def principal (argv):
    nbArgs = len(sys.argv)

#    if nbArgs >= 3:
#        nomFichALire = sys.argv[1]
#        nomFichAEcrire = sys.argv[2]
#    else:
#        print("*** Il faut donner en arg. le nom des fichiers lu et ecrit.")
#        sys.exit(1)

    graine = fabriqueTempsSyntaxeGraine()
    nbBitsFournis = len(graine) * 6
    print("La graine est [%s], soit assez pour %d bits." % (graine, nbBitsFournis))

    nbCellules = 137
    ligneShell = "./longtun2 %d %s 100000000 500 > resultat_longtun2.txt" % (nbCellules, graine)
    print(ligneShell)
    system(ligneShell)
    ligneShell = "./analyse_tunnel.py resultat_longtun2.txt"
    print(ligneShell)
    system(ligneShell)

    time.sleep(2.0) # A tout hasard, pour ne pas venir trop vite apres les requetes
                    # d'analyse_tunnel.py
    # lanceSinodoju () # On va laisser courteline s'occuper de relancer amarelia

def alimenteBaseDeDonnees (chaineTemps, serveurLocal, serveurDistant):
    mesEnvoisPost = {
               'nom': chaineTemps,
               'param1': ("Je suis sur %s."  % (serveurLocal)),
               'param2': ("Je passe la main à %s." % (serveurDistant)),
               'param3': "Je n'ai rien à ajouter.",
              }
    params = urlencode(mesEnvoisPost, quote_via=quote_plus)

    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

    conn = http.client.HTTPConnection("jlancey.alwaysdata.net:80")

    conn.request("POST", "/dialogue/url-mimine-post", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    # print(data)

    conn.close()

def fabriqueTempsSyntaxeUrl ():
    # tempsSyntaxeUrl = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
    tempsSyntaxeUrl = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    return tempsSyntaxeUrl

def fabriqueTempsSyntaxeGraine ():
    graine = time.strftime("ancey%Y%m%da%Hh%Mm%S", time.localtime())

    return graine

def lanceSinodoju ():
    conn = http.client.HTTPConnection("www.amarelia.ch")

    conn.request("GET", "/sinodoju/sinodoju.php")

    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    data1 = r1.read()
    # print(data1)

    conn.close()

# --- Fin des definitions de classes et de fonctions,
# --- debut du programme principal

principal(sys.argv)
