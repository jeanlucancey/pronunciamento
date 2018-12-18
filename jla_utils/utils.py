# import sys


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
