import sys
from os import system

from django.http import (Http404, HttpResponse)
from django.template import Context, loader
from django.shortcuts import (get_object_or_404, \
                              redirect, \
                              # render_to_response, \
                              render)
from django.views.generic import View # Pour faire des class-based views, voir p. 255

from blog.models import Post
from .models import Categorie, Photo
from .forms import CategorieForm, PhotoForm


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
    message = "J'ai quétchoze à dire, et ce que j'ai à dire, " + \
              "c'est que c'est moi le chef, pas ce connard de Django!"
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

def importeCategories(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Ceci est voué à remplir la table des categories à partir d'un fichier CSV.</p>\n"
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

def importePhotos(request):
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Ceci est voué à remplir la table des photos à partir d'un fichier CSV.</p>\n"
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

# Ce qui suit a ete neutralise au profit d'une class-based view, voir p. 255
#def listeCategories4(request):
# Variante de la variante précédente (celle avec des #), employant le shortcut render
# au lieu du shortcut render_to_response (ca fait plus de trucs
# supposes utiles quoique au prix d'une degradation des temps de réponse).
# Ce n'est donc pas vraiment equivalent ni a listeCategories3 ni surout à listeCategories2,
# à mon grand désespoir car listeCategories2 me paraît beaucoup plus clair
# et souple. Voir Pinkham 5.6.3 p. 139
#    return render(request, \
#                  'cestmoilechef/categorie_list.html', \
#                  {'categorie_list': Categorie.objects.all()})

# Remplacement de la fonction précédente par une class-based view
class CategorieList(View):
    def get(self, request):
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

def categorie_detail_pabon2(request, slugUrl):
# Pour rendre les choses plus claires et ne pas écrire des horreurs du genre
# slug=slug, je distingue slug (attribut d'une catégorie) et slugUrl (la
# mention écrite dans l'URL)
    try:
        categorie = Categorie.objects.get(slug__iexact = slugUrl)
    except Categorie.DoesNotExist:
        raise Http404
    pageEntiere = ""
    pageEntiere += "<html>\n"
    pageEntiere += "<body>\n"
    pageEntiere += "<p>Cette page cherche juste à vérifier que le slug est bien compris.</p>\n"
    pageEntiere += "<p>slug est une variable et vaut&nbsp;: [%s]</p>\n" % (slugUrl)
    pageEntiere += "<p>categorie.nom vaut&nbsp;: [%s]</p>\n" % (categorie.nom)
    pageEntiere += "<p>categorie.slug vaut&nbsp;: [%s]</p>\n" % (categorie.slug)
    pageEntiere += "</body>\n"
    pageEntiere += "</html>\n"
    return HttpResponse(pageEntiere)

def categorie_detail(request, slugUrl):
# Voir ci-dessous categorie_detail_shortcut, une version abrégée qui fait
# la même chose avec un shortcut, et aussi categorie_detail_shortcut2, qui
# fait un petit peu plus avec deux shortcuts, ce qui est sûrement plus
# orthodoxe et recommandé par les bonnes pratiques mais imbitable et
# in-modifiable, à mon grand désespoir.
    try:
        categorie = Categorie.objects.get(slug__iexact = slugUrl)
    except Categorie.DoesNotExist:
        raise Http404
    template = loader.get_template('cestmoilechef/categorie_detail.html')
    context = Context({'categorie': categorie})
    output = template.render(context)
    return HttpResponse(output)

# def categorie_detail_shortcut(request, slugUrl):
# Rigoureusement la même chose que la fonction précédente, mais avec un shortcut
#    categorie = get_object_or_404(Categorie, slug__iexact = slugUrl)
#    template = loader.get_template('cestmoilechef/categorie_detail.html')
#    context = Context({'categorie': categorie})
#    output = template.render(context)
#    return HttpResponse(output)

def categorie_detail_shortcut2(request, slugUrl):
# Un petit peu plus que la version précédente, et donc que categorie_detail
# que pourtant je trouve beaucoup plus claire et plus souple.
# Voir Pinkham 5.6.3 p. 139
    categorie = get_object_or_404(Categorie, slug__iexact = slugUrl)
    return render(request, \
                  'cestmoilechef/categorie_detail.html', \
                  {'categorie': categorie})

def montrePhotoPrecise(request, nomPhotoUrl):
    maPhoto = get_object_or_404(Photo, nomAbrege__iexact = nomPhotoUrl)
    template = loader.get_template('cestmoilechef/photo_precise.html')
    context = Context({'photo': maPhoto})
    output = template.render(context)
    return HttpResponse(output)

# Je crois bien que la méthode qui suit est caduque, vu que Pinkham lui
# substitue la class-based view CategorieCreate en 9.2.2.3 p. 246,
# mais c'est sa façon de faire à lui et il signale qu'écrire quelque chose
# du genre de categorie_create est ce qui est préconisé dans la plupart
# des tutoriels, donc il vaut mieux garder ce code à titre de référence.
def categorie_create(request):
# Pompé sur Pinkham, p. 244. Le style n'est pas le mien et il n'est
# pas vraiment aimé par Pinkham, qui le signale juste comme de pratique standard.
# En tout cas, je signale qu'il y a deux return a l'intérieur de boucles if, et
# non pas un seul à la fin de la méthode, comme je fais d'ordinaire.
    if request.method == 'POST':
        # bind data to form
        form = CategorieForm(request.POST)
        # if the data is valid:
        if form.is_valid(): # L'appel de cette méthode crée errors et cleaned_data
            # create new object from data
            new_categorie = form.save()
            return redirect(new_categorie)
            # show webpage for new objects
        # else implicite: form contient des données invalides
    else: # request.method != 'POST'
        # show unbound HTML form
        form = CategorieForm()
    return render(
                  request,
                  'cestmoilechef/categorie_form.html',
                  {'form': form}
                 )

class CategorieCreate(View):
    form_class = CategorieForm
    template_name = 'cestmoilechef/categorie_form.html'

    def get(self, request):
        return render(
                         request,
                         self.template_name,
                         {'form': self.form_class()}
                     )

    def post(self, request):
    # Attention, code façon Pinkham, avec deux return dans une boucle if
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_categorie = bound_form.save()
            return redirect(new_categorie)
        else:
            return render(
                             request,
                             self.template_name,
                             {'form': bound_form}
                         )

class PhotoUpdate(View): # Inspiré de la p. 259
    form_class = PhotoForm
    model = Photo
    template_name = 'cestmoilechef/photo_form_update.html'

    def get_object(self, nomPhotoArg):
        return get_object_or_404(
                                 self.model,
                                 nomAbrege=nomPhotoArg
                                )

    def get(self, request, nomPhotoUrl):
        maPhoto = self.get_object(nomPhotoUrl)
        context = {
                   'form': self.form_class(instance=maPhoto),
                   'photo': maPhoto,
                  }
        return render(request, self.template_name, context)

    def post(self, request, nomPhotoUrl):
        maPhoto = self.get_object(nomPhotoUrl)
        bound_form = self.form_class(
                                     request.POST,
                                     instance=maPhoto
                                    )
        if bound_form.is_valid():
            new_photo = bound_form.save()
            return redirect(new_photo)
        else:
            context = {
                       'form': bound_form,
                       'photo': maPhoto,
                      }
        return render(
                      request,
                      self.template_name,
                      context
                     )

class PhotoDelete(View): # Inspiré de la p. 270
    def get(self, request, nomPhotoUrl):
        maPhoto = get_object_or_404(
                                       Photo,
                                       nomAbrege = nomPhotoUrl
                                   )
        return render(request,
                      'cestmoilechef/photo_confirm_delete.html',
                      {'photo': maPhoto}
                     )

    def post(self, request, nomPhotoUrl):
        maPhoto = get_object_or_404(
                                       Photo,
                                       nomAbrege = nomPhotoUrl
                                   )
        maPhoto.delete()
        return redirect('liste_pho_tos_2')

class PhotoCreate(View):
    form_class = PhotoForm
    template_name = 'cestmoilechef/photo_form.html'

    def get(self, request):
        return render(
                         request,
                         self.template_name,
                         {'form': self.form_class()}
                     )

    def post(self, request):
    # Attention, code façon Pinkham, avec deux return dans une boucle if
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_photo = bound_form.save()
            return redirect(new_photo)
        else:
            return render(
                             request,
                             self.template_name,
                             {'form': bound_form}
                         )

class CategorieDelete(View):
    def get(self, request, slugUrl):
        maCategorie = get_object_or_404(
                                           Categorie,
                                           slug__iexact = slugUrl
                                           # slug au lieu de slug__iexact marcherait
                                        )
        return render(request,
                      'cestmoilechef/categorie_confirm_delete.html',
                      {'categorie': maCategorie}
                     )

    def post(self, request, slugUrl):
        maCategorie = get_object_or_404(
                                       Categorie,
                                       slug__iexact = slugUrl
                                       # slug au lieu de slug__iexact marcherait
                                   )
        maCategorie.delete()
        return redirect('liste_cate_gories_2')

class CategorieUpdate(View):
    form_class = CategorieForm
    model = Categorie
    template_name = 'cestmoilechef/categorie_form_update.html'

    def get_object(self, slugArg):
        return get_object_or_404(
                                 self.model,
                                 slug=slugArg
                                )

    def get(self, request, slugUrl):
        maCategorie = self.get_object(slugUrl)
        context = {
                   'form': self.form_class(instance=maCategorie),
                   'categorie': maCategorie,
                  }
        return render(request, self.template_name, context)

    def post(self, request, slugUrl):
        maCategorie = self.get_object(slugUrl)
        bound_form = self.form_class(
                                     request.POST,
                                     instance=maCategorie
                                    )
        if bound_form.is_valid():
            new_categorie = bound_form.save()
            return redirect(new_categorie)
        else:
            context = {
                       'form': bound_form,
                       'categorie': maCategorie,
                      }
        return render(
                      request,
                      self.template_name,
                      context
                     )
