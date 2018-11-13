from django.http import HttpResponse
import sys
from os import system
from blog.models import Post

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
            octet = ligneAEcrire2[numOctet:numOctet + 1] # pour que ce soit du type "bytes"
            self.ecritUnOctet(octet)
        self.ecritUnOctet(b'\n')

    def ecritUnOctet (self, octet):
        self.fichier.seek(self.index, 0)
        self.fichier.write(octet)
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

        ligneLue2 = deByteStringAChaineUnicode(ligneLue)
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
    pageEntiere += "</p>\n"
    pageEntiere += echoPath()
    pageEntiere += multiplication()
    pageEntiere += lsLong()
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def imagePorte(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Merci bien.</p>\n"
    pageEntiere += "<center><img src=\"http://courteline.org/hotes/portes_todito/porte230.jpg\" width=480 height=640></center>\n"
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def vignettes(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p><a href=\"http://courteline.org/hotes/vignettes/\">Accès à la page des vignettes</a></p>\n"
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def exportePosts(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Ceci est voué à permettre l'exportation des posts.</p>\n"
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    monFichier = Fichier("posts_exportes.txt", True)
    mesPosts = Post.objects.all()
    nbPosts = Post.objects.count()
    for numPost in range(nbPosts):
        monPost = mesPosts[numPost]
        monTitre = monPost.title
        monFichier.ecritUneLigne(monTitre)
        monTexte = monPost.text
        monFichier.ecritUneLigne(monTexte)
        if numPost < nbPosts - 1:
            monFichier.ecritUneLigne("")
    monFichier.close()
    return HttpResponse(pageEntiere)
