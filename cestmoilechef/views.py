from django.http import HttpResponse
import sys
from os import system


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

        
def echoPath():        
    blabla = ""
    system("echo $PATH > deleatur.txt")
    monFichier = Fichier("deleatur.txt", False)
    while monFichier.index < monFichier.longueur:
        ligneLue = monFichier.litUneLigne()
        ligneAEcrire = "<p>%s</p>\n" % (ligneLue)
        blabla += ligneAEcrire
    monFichier.close()
    return blabla

def lsLong():
    blabla = ""
    system("ls -l > deleatur.txt")
    monFichier = Fichier("deleatur.txt", False)
    while monFichier.index < monFichier.longueur:
        ligneLue = monFichier.litUneLigne()
        ligneAEcrire = "<p>%s</p>\n" % (ligneLue)
        blabla += ligneAEcrire
    monFichier.close()
    return blabla

def multiplication():
    blabla = ""
    maxMultiplicande = 3
    maxMultiplicateur = 2
    for multiplicande2 in range(maxMultiplicande):
        multiplicande = multiplicande2 + 1
        for multiplicateur2 in range(maxMultiplicateur):
            multiplicateur = multiplicateur2 + 1
            blabla += "<p>%d * %d = %d</p>\n" % (multiplicande, multiplicateur, \
                                          multiplicande * multiplicateur)
            if multiplicateur2 == maxMultiplicateur - 1:
                blabla += "<p>&nbsp;</p>\n"
    return blabla

def pronunciamento(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>"
    pageEntiere += "Que ce soit bien clair&nbsp;: a partir de maintenant, "
    pageEntiere += "c'est <strong>moi, Timoleon Bludugudule</strong>, le chef, "
    pageEntiere += "et ca va chier."
    pageEntiere += echoPath()
    pageEntiere += multiplication()
    pageEntiere += lsLong()
    pageEntiere += "</p>\n"
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)
