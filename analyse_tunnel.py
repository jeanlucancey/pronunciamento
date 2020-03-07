#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import time
import sys
from os import system
import httplib, urllib
import base64

# IMPORTANT - Ce listing fait partie du projet Django tout
# en n'en faisant pas partie... Il n'est pas lancé par Django
# lui-même mais par "sinodoju2.py", lui-même lancé par une commande
# "system" dans un fichier "views.py" (de Django cette fois, et même
# de l'application "dialogue" au moment où j'écris ces lignes).
# Non, ce n'est pas n'importe quoi: c'est parce que cette bidouille
# est vouée à être également lancée sur d'autres serveurs, en dépendant
# cette fois de scripts PHP... sans Django, donc. Pour permettre une
# homogénéité de traitement entre mon serveur Django chez AlwaysData
# et mes serveurs PHP chez Phpnet et Alphosting-Tizoo, j'utilise à
# peu près le même listing dans les trois cas (il y a des variantes
# subtiles). Mais du coup c'est mon Django qui n'est plus totalement
# homogène... Tant pis. Je suis un adepte des bricolages quick and
# dirty et je vous emmerde. :-P

# --- Definitions de classes

class Tunnel:
    def __init__(self, longueurArg, generationArg):
        self.longueur = longueurArg
        self.generation = generationArg

class Fichier:
    def __init__(self, nomFichierArg, boolEcriture):
        self.nomFichier = nomFichierArg
        if boolEcriture:
            self.fichier = open(self.nomFichier, 'w')
            self.fichier.seek(0, 0) # Se place au debut du fichier
            self.longueur = 0
        else:
            self.fichier = open(self.nomFichier, 'r')
            self.fichier.seek(0, 2) # Se place a la fin du fichier
            self.longueur = self.fichier.tell()
        self.index = 0

    def close (self):
        self.fichier.close()

    def ecritUneLigne (self, ligneAEcrire):
        for numSigne in range(len(ligneAEcrire)):
            signe = ligneAEcrire[numSigne]
            self.ecritUnOctet(signe)
        self.ecritUnOctet('\n')

    def ecritUnOctet (self, signe):
        self.fichier.seek(self.index, 0)
        self.fichier.write(signe)
        self.index += 1
        self.longueur += 1

    def interromptLecture (self):
        self.close()

    def litUneLigne (self):
        octetLu = ''
        ligneLue = ''
        finDeLigne = 0 # false

        while self.index < self.longueur and not finDeLigne:
            octetLu = self.litUnOctet(self.index)
            if octetLu == '\n':
                finDeLigne = 1 # true
            else:
                ligneLue += octetLu

        return ligneLue

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

    if nbArgs >= 2:
        nomFichTunnel = sys.argv[1]
    else:
        print "*** Il faut donner en arg. le nom d'un fichier produit par longtun2."
        sys.exit(1)

    numLigneLue = 0
    fichALire = Fichier(nomFichTunnel, 0)
    chouBlanc = True # Par defaut
    nbCell = 0
    graine = ""
    mesTunnels = []
    while fichALire.index < fichALire.longueur:
        ligneLue = fichALire.litUneLigne()
        numLigneLue += 1
        if numLigneLue == 1:
            nbCell = analyseNbCell(ligneLue)
        elif numLigneLue == 2:
            graine = analyseGraine(ligneLue)
        else:
            if (len(ligneLue) > 10) and (ligneLue[0:6] == "Tunnel"):
                chouBlanc = False
                monTunnelNormalise = analyseTunnel(ligneLue)
                mesTunnels.append(monTunnelNormalise)
    fichALire.close()
    print("Le nombre de cellules est de %d." % (nbCell))
    print("La graine est [%s]." % (graine))

    nomEntreeDeBase = fabriqueTempsSyntaxeUrl()
    identifiantSerpicon = "%d %s" % (nbCell, graine)
    nomServeur = "alwaysdata"

    if chouBlanc:
        alimenteBaseDeDonnees(nomEntreeDeBase, identifiantSerpicon, "Chou blanc !", nomServeur)
    else:
        for numTunnel in range(len(mesTunnels)):
            monTunnel = mesTunnels[numTunnel]
            maLongueur = monTunnel.longueur
            maGeneration = monTunnel.generation
            print("Tunnel de %s a la generation %s" % \
                 (separateurMille(maLongueur, ' '),
                  separateurMille(maGeneration, ' ')))
            nomEntreeDeBase = fabriqueTempsSyntaxeUrl()
            nomEntree = nomEntreeDeBase + "__" + separateurMille(maLongueur, '_')
            descriptifTunnel = separateurMille(maLongueur, ' ') + " en " \
                               + separateurMille(maGeneration, ' ')
            alimenteBaseDeDonnees(nomEntree, identifiantSerpicon, descriptifTunnel, nomServeur)
            if numTunnel < len(mesTunnels) - 1:
                attend(5.0)

def alimenteBaseDeDonnees (nomEntree, identifiantSerpicon, descriptifTunnel, serveur):
    mesEnvoisPost = {
               'nom': nomEntree,
               'param1': identifiantSerpicon,
               'param2': descriptifTunnel,
               'param3': serveur,
              }
    params = urllib.urlencode(mesEnvoisPost)

    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

    conn = httplib.HTTPConnection("jlancey.alwaysdata.net:80")

    conn.request("POST", "/dialogue/url-mimine-post", params, headers)

    response = conn.getresponse()
    # print(response.status, response.reason)
    # (En principe, quand ca marche, response.status doit valoir 200 et
    # response.reason valoir 'OK'; une erreur possible serait que
    # response.status vaille 500 et response.reason 'INTERNAL SERVER ERROR'...
    # mais pour le moment je vais considerer que le probleme ne se pose pas)

    data = response.read() # Je n'en fais rien, mais bon

    conn.close()

def analyseGraine (ligneLue):
    graine = ligneLue[10:len(ligneLue) - 1]

    return graine

def analyseNbCell (ligneLue):
    nbCellString = ligneLue[9:len(ligneLue)]
    nbCell = int(nbCellString)

    return nbCell

def analyseTunnel (ligneLue):
    chaineLongueur = ""
    chaineGeneration = ""
    caracLu = ""
    numSigne = 10
    eTrouve = False
    while (not eTrouve) and (numSigne < len(ligneLue)):
        signeLu = ligneLue[numSigne]
        if signeLu == "e":
            eTrouve = True
        else:
            chaineLongueur += signeLu
        numSigne += 1
    chaineLongueur = chaineLongueur[0:len(chaineLongueur) - 1] # pour virer l'espace finale
    maLongueur = int(vireSigne(chaineLongueur, ' '))
    numSigne += 2
    chaineGeneration = ligneLue[numSigne:len(ligneLue)]
    maGene = int(vireSigne(chaineGeneration, ' '))

    monTunnel = Tunnel(maLongueur, maGene)

    return monTunnel

def attend (dureeEnSecondes):
    time.sleep(dureeEnSecondes)

def fabriqueTempsSyntaxeUrl ():
    # tempsSyntaxeUrl = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
    tempsSyntaxeUrl = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    return tempsSyntaxeUrl

def separateurMille (monEntier, monSeparateur):
    maChaine0 = "%d" % (monEntier)
    maChaine1 = ""
    for numSigne in range(len(maChaine0)):
        numSigne2 = len(maChaine0) -1 - numSigne
        monSigne = maChaine0[numSigne2]
        if (numSigne % 3 == 0) and numSigne > 0:
            maChaine1 = monSeparateur + maChaine1
        maChaine1 = monSigne + maChaine1

    return maChaine1

def vireSigne (maChaine, monSigneAVirer):
    maChainePurgee = ""
    for numSigne in range(len(maChaine)):
        monSigne = maChaine[numSigne]
        if monSigne != monSigneAVirer:
            maChainePurgee += monSigne

    return maChainePurgee


# --- Fin des definitions de classes et de fonctions,
# --- debut du programme principal

principal(sys.argv)
