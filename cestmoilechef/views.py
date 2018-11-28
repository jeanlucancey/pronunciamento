from django.http import (Http404, HttpResponse)
import sys
from os import system
from blog.models import Post
from .models import Categorie, Photo
from django.template import Context, loader
from django.shortcuts import (get_object_or_404, \
                              # render_to_response, \
                              render)


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
#    pageEntiere = ""
#    pageEntiere += "<html>\n"
#    pageEntiere += "<body>\n"
#    pageEntiere += "<p>"
#    pageEntiere += "Que ce soit bien clair&nbsp;: a partir de maintenant, "
#    pageEntiere += "c'est <strong>moi, Timoleon Bludugudule</strong>, le chef, "
#    pageEntiere += "et ca va chier."
#    pageEntiere += "</p>\n"
#    pageEntiere += echoPath()
#    pageEntiere += multiplication()
#    pageEntiere += lsLong()
#    pageEntiere += "</body>\n"
#    pageEntiere += "</html>\n"
    template = loader.get_template('cestmoilechef/pronunciamento.html')
    message = "C'est pas parce qu'on n'a rien à dire qu'il faut fermer sa gueule."
    context = Context({'message': message})
    output = template.render(context)
    return HttpResponse(output)

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

def vireGuill (mention):
    if mention[0] == '"' and mention[len(mention) - 1] == '"':
        mention = mention[1:len(mention) - 1]
    return mention

def creeCategories(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Ceci est voué à permettre la creation des categories à partir d'un fichier CSV.</p>\n"
    monFichier = Fichier("categories.csv", False)
    while monFichier.index < monFichier.longueur:
        ligneLue = monFichier.litUneLigne()
        ligneAEcrire = "<p>%s</p>" % (ligneLue)
        pageEntiere += ligneAEcrire
        mesBazars = ligneLue.split(',')
        monNom = vireGuill(mesBazars[0])
        monSlug = vireGuill(mesBazars[1])
        ligneAEcrire = "<p>[%s] - [%s]</p>" % (monNom, monSlug)
        pageEntiere += ligneAEcrire
        # Je neutralise ce qui suit parce que ca a marche et que ce n'est
        # pas voue a etre utilise deux fois
        # Categorie.objects.create(nom=monNom, slug=monSlug)
    monFichier.close()
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def listeCategories(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Voici la liste des catégories incluses dans la base "
    pageEntiere += "(nom complet, puis slug).</p>\n"
    mesCategories = Categorie.objects.all()
    nbCategories = Categorie.objects.count()
    for numCategorie in range(nbCategories):
        maCategorie = mesCategories[numCategorie]
        monNom = maCategorie.nom
        monSlug = maCategorie.slug
        ligneAEcrire = "<p>[%s] - [%s]</p>\n" % (monNom, monSlug)
        pageEntiere += ligneAEcrire
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def creePhotos(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Ceci est voué à permettre la creation des photos à partir d'un fichier CSV.</p>\n"
    monFichier = Fichier("portes_classees.csv", False)
    while monFichier.index < monFichier.longueur:
        ligneLue = monFichier.litUneLigne()
        ligneAEcrire = "<p>%s</p>" % (ligneLue)
        pageEntiere += ligneAEcrire
        mesBazars = ligneLue.split(',')
        monNomAbrege = vireGuill(mesBazars[0])
        maCategEnClair = vireGuill(mesBazars[1])
        maCategEnVrai = Categorie.objects.get(slug=maCategEnClair)
        monPathEtNom = vireGuill(mesBazars[2])
        ligneAEcrire = "<p>[%s]</p>" % (maCategEnClair)
        pageEntiere += ligneAEcrire
        # Je neutralise ce qui suit parce que ca a marche et que ce n'est
        # pas voue a etre utilise deux fois. A noter que certes ca a
        # marche, mais que ca a aussi considerablement ramé.
        # Photo.objects.create(nomComplet=monPathEtNom, nomAbrege=monNomAbrege, categorie=maCategEnVrai)
    monFichier.close()
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def listePhotos(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Voici la liste des photos incluses dans la base "
    pageEntiere += "(nom abrégé, catégorie, puis nomEntier).</p>\n"
    mesPhotos = Photo.objects.all()
    nbPhotos = Photo.objects.count()
    for numPhoto in range(nbPhotos):
        maPhoto = mesPhotos[numPhoto]
        monNomAbrege = maPhoto.nomAbrege
        monNomComplet = maPhoto.nomComplet
        maCateg = maPhoto.categorie.slug
        ligneAEcrire = "<p>[%s] - [%s] - [%s]</p>\n" % (monNomAbrege, maCateg, monNomComplet)
        pageEntiere += ligneAEcrire
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def purgePhotos(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Cette page radioactive est vouée à détruire les photos de la base.</p>\n"
    mesPhotos = Photo.objects.all()
    nbPhotos = Photo.objects.count()
    for numPhoto in range(nbPhotos - 1, -1, -1):
        maPhoto = mesPhotos[numPhoto]
        monNomAbrege = maPhoto.nomAbrege
        monNomComplet = maPhoto.nomComplet
        maCateg = maPhoto.categorie.slug
        ligneAEcrire = "<p>%d - [%s] - [%s] - [%s]</p>\n" % (numPhoto, monNomAbrege, maCateg, monNomComplet)
        pageEntiere += ligneAEcrire
        # Je neutralise la ligne qui suit, par prudence
        # maPhoto.delete()
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def listeCategories2(request):
# Fonction écrite sans shortcuts, et que je trouve beaucoup plus claire et souple,
# mais que Pinkham recommande de remplacer par listeCategories3 ou plutôt
# listeCategories4
    categorie_list = Categorie.objects.all()
    template = loader.get_template('cestmoilechef/categorie_list.html')
    context = Context({'categorie_list': categorie_list})
    output = template.render(context)
    return HttpResponse(output)

# def listeCategories3(request):
# Variante de la fonction précédente, avec shortcuts et nonobstant
# deja obsolete car render tend a remplacer render_to_response (ca fait
# plus de trucs au prix d'une degradation des temps de réponse).
# Perso moi-je, je trouve ça de toute façon beaucoup moins clair
# et de surcroît pas souple du tout. Voir Pinkham 5.6.3 p. 139
#     return render_to_response('cestmoilechef/categorie_list.html',
#                               {'categorie_list': Categorie.objects.all()})

def listeCategories4(request):
# Variante de la variante précédente (celle avec des #), employant le shortcut render
# au lieu du shortcut render_to_response (ca fait plus de trucs
# supposes utiles quoique au prix d'une degradation des temps de réponse).
# Ce n'est donc pas vraiment equivalent ni a listeCategories3 ni surout à listeCategories2,
# à mon grand désespoir car listeCategories2 me paraît beaucoup plus clair
# et souple. Voir Pinkham 5.6.3 p. 139
    return render(request, \
                  'cestmoilechef/categorie_list.html', \
                  {'categorie_list': Categorie.objects.all()})

def listePhotos2(request):
# Fonction écrite sans shortcuts, et que je trouve beaucoup plus claire et souple,
# mais que Pinkham recommande de remplacer par listePhotos3 ou plutôt listePhotos4
    photo_list = Photo.objects.all()
    template = loader.get_template('cestmoilechef/photo_list.html')
    context = Context({'photo_list': photo_list})
    output = template.render(context)
    return HttpResponse(output)

# def listePhotos3(request):
# Variante de la fonction précédente, avec shortcuts et nonobstant
# deja obsolete car render tend a remplacer render_to_response (ca fait
# plus de trucs au prix d'une degradation des temps de réponse).
# Perso moi-je, je trouve ça de toute façon beaucoup moins clair
# et de surcroît pas souple du tout. Voir Pinkham 5.6.3 p. 139
#     return render_to_response('cestmoilechef/photo_list.html',
#                               {'photo_list': Photo.objects.all()})

def listePhotos4(request):
# Variante de la variante précédente (celle avec des #), employant le shortcut render
# au lieu du shortcut render_to_response (ca fait plus de trucs
# supposes utiles quoique au prix d'une degradation des temps de réponse).
# Ce n'est donc pas vraiment equivalent ni a listePhotos3 ni surout à listePhotos2,
# à mon grand désespoir car listePhotos2 me paraît beaucoup plus clair
# et souple. Voir Pinkham 5.6.3 p. 139
    return render(request, \
                  'cestmoilechef/photo_list.html', \
                  {'photo_list': Photo.objects.all()})

def categorie_detail_pabon(request):
    # Comme l'explique Pinkham au bas de la page 129, on peut faire
    # ce que je fais ici, mais c'est moche et pas propre. Ca fait rien,
    # ca me parait pedagogique.
    monFullPath = request.path_info # Et cette variable, on la bidouille comme on veut
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Cette page cherche juste à montrer que l'URL peut être bidouillée à la mimine.</p>\n"
    pageEntiere += "<p>monFullPath est une variable et vaut&nbsp;: [%s]</p>\n" % (monFullPath)
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def categorie_detail_pabon2(request, slug):
    try:
        categorie = Categorie.objects.get(slug__iexact = slug)
    except Categorie.DoesNotExist:
        raise Http404
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Cette page cherche juste à vérifier que le slug est bien compris.</p>\n"
    pageEntiere += "<p>slug est une variable et vaut&nbsp;: [%s]</p>\n" % (slug)
    pageEntiere += "<p>categorie.nom vaut&nbsp;: [%s]</p>\n" % (categorie.nom)
    pageEntiere += "<p>categorie.slug vaut&nbsp;: [%s]</p>\n" % (categorie.slug)
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def categorie_detail(request, slug):
# Voir ci-dessous categorie_detail_shortcut, une version abrégée qui fait
# la même chose avec un shortcut, et aussi categorie_detail_shortcut2, qui
# fait un petit peu plus avec deux shortcuts, ce qui est sûrement plus
# orthodoxe et recommandé par les bonnes pratiques mais imbitable et
# in-modifiable, à mon grand désespoir.
    try:
        categorie = Categorie.objects.get(slug__iexact = slug)
    except Categorie.DoesNotExist:
        raise Http404
    template = loader.get_template('cestmoilechef/categorie_detail.html')
    context = Context({'categorie': categorie})
    output = template.render(context)
    return HttpResponse(output)

def categorie_detail_shortcut(request, slug):
# Rigoureusement la même chose que la fonction précédente, mais avec un shortcut
    categorie = get_object_or_404(Categorie, slug__iexact = slug)
    template = loader.get_template('cestmoilechef/categorie_detail.html')
    context = Context({'categorie': categorie})
    output = template.render(context)
    return HttpResponse(output)

def categorie_detail_shortcut2(request, slug):
# Un petit peu plus que la version précédente, et donc que categorie_detail
# que pourtant je trouve beaucoup plus claire et plus souple.
# Voir Pinkham 5.6.3 p. 139
    categorie = get_object_or_404(Categorie, slug__iexact = slug)
    return render(request, \
                  'cestmoilechef/categorie_detail.html', \
                  {'categorie': categorie})

def montrePhotoPrecise(request, nomPhoto):
    template = loader.get_template('cestmoilechef/photo_precise.html')
    context = Context({'nomPhoto': nomPhoto})
    output = template.render(context)
    return HttpResponse(output)
