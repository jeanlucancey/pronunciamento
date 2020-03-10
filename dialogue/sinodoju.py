import time

from os import system

from django.http import HttpResponse
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt # Pour des formulaires POST libres

from jla_utils.utils import Fichier
from .models import ElementDialogue

class Tunnel:
    def __init__(self, longueurArg, generationArg):
        self.longueur = longueurArg
        self.generation = generationArg

def alimenteBaseDeDonnees (nomEntree, identifiantSerpicon, descriptifTunnel, serveur):
    ElementDialogue.objects.create(
                                      nom = nomEntree,
                                      param1 = identifiantSerpicon,
                                      param2 = descriptifTunnel,
                                      param3 = serveur
                                  )

def analyseGraine (ligneLue):
    graine = ligneLue[10:len(ligneLue) - 1]

    return graine

def analyseNbCell (ligneLue):
    nbCellString = ligneLue[9:len(ligneLue)]
    nbCell = int(nbCellString)

    return nbCell

def analyseTunnel (request):
    nomFichTunnel = "resultat_longtun2.txt"
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
                monTunnelNormalise = analyseTunnelMoteur(ligneLue)
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

    # time.sleep(2.0) # A tout hasard, pour ne pas venir trop vite apres les requetes
                    # d'analyse_tunnel.py
    # lanceSinodoju () # On va laisser courteline s'occuper de relancer amarelia

    tableauDeLignes = []
    tableauDeLignes.append("Cette page est la page de l'analyse des tunnels.")

    template = loader.get_template('cestmoilechef/petite_merdasse.html')
    context = Context({ 'tabDeLignes': tableauDeLignes })
    output = template.render(context)
    return HttpResponse(output)

def attend (dureeEnSecondes):
    time.sleep(dureeEnSecondes)

def analyseTunnelMoteur (ligneLue):
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

def fabriqueTempsSyntaxeGraine ():
    graine = time.strftime("ancey%Y%m%da%Hh%Mm%S", time.localtime())

    return graine

def fabriqueTempsSyntaxeUrl ():
    # tempsSyntaxeUrl = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
    tempsSyntaxeUrl = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    return tempsSyntaxeUrl

def lanceSinodoju ():
    conn = http.client.HTTPConnection("www.amarelia.ch")

    conn.request("GET", "/sinodoju/sinodoju.php")

    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    data1 = r1.read()
    # print(data1)

    conn.close()

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

@csrf_exempt # En théorie, c'est une brèche de sécurité; en pratique... ca depend
def viewSinodoju (request):
    tableauDeLignes = []
    tableauDeLignes.append("Cette page est la page de Sinodoju.")

    graine = fabriqueTempsSyntaxeGraine()
    nbBitsFournis = len(graine) * 6
    tableauDeLignes.append("La graine est [%s], soit assez pour %d bits." % (graine, nbBitsFournis))

    nbCellules = 137
    system("./sinodoju.pl %d %s > cr_perl.txt 2> cr2_perl.txt &" % (nbCellules, graine))

    tableauDeLignes.append("En principe, si vous lisez ça, c'est qu'un daemon Sinodoju a été lancé.")
    tableauDeLignes.append("Donc ça aura un effet... quand le daemon aura fini de travailler,")
    tableauDeLignes.append("mais ce template vous rend la main tout de suite.")

    template = loader.get_template('cestmoilechef/petite_merdasse.html')
    context = Context({ 'tabDeLignes': tableauDeLignes })
    output = template.render(context)
    return HttpResponse(output)

def vireSigne (maChaine, monSigneAVirer):
    maChainePurgee = ""
    for numSigne in range(len(maChaine)):
        monSigne = maChaine[numSigne]
        if monSigne != monSigneAVirer:
            maChainePurgee += monSigne

    return maChainePurgee
