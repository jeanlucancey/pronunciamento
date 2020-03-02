from os import system

from django.http import (Http404, HttpResponse)
from django.template import Context, loader
from django.shortcuts import (get_object_or_404, \
                              redirect, \
                              # render_to_response, \
                              render)
from django.views.generic import View # Pour faire des class-based views, voir p. 255
from django.views.decorators.csrf import csrf_exempt # Pour des formulaires POST libres

from jla_utils.utils import Fichier

from .models import ElementDialogue
from .forms import ElementDialogueForm

def accueilDialogue(request):
    template = loader.get_template('dialogue/accueil.html')
    message = "Je veux juste pouvoir noter quelques paramètres quelque part."
    context = Context({'message': message})
    output = template.render(context)
    return HttpResponse(output)

def vireGuill (mention):
    if mention[0] == '"' and mention[len(mention) - 1] == '"':
        mention = mention[1:len(mention) - 1]
    return mention

class DialogueList(View):
    def get(self, request):
        return render(request, \
                      'dialogue/liste.html', \
                      {'dialogue_list': ElementDialogue.objects.all()})

class ElementDialogueCreate(View):
    form_class = ElementDialogueForm
    template_name = 'dialogue/element_form.html'

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
            new_element = bound_form.save()
            return redirect(new_element)
        else:
            return render(
                             request,
                             self.template_name,
                             {'form': bound_form}
                         )

def elementDialogueDetail(request, nomUrl):
    try:
        monElement = ElementDialogue.objects.get(nom__iexact = nomUrl)
    except ElementDialogue.DoesNotExist:
        raise Http404
    template = loader.get_template('dialogue/element_detail.html')
    context = Context({'element': monElement})
    output = template.render(context)
    return HttpResponse(output)

class ElementDialogueUpdate(View):
    form_class = ElementDialogueForm
    model = ElementDialogue
    template_name = 'dialogue/element_form_update.html'

    def get_object(self, nomArg):
        return get_object_or_404(
                                 self.model,
                                 nom=nomArg
                                )

    def get(self, request, nomUrl):
        monElement = self.get_object(nomUrl)
        context = {
                   'form': self.form_class(instance=monElement),
                   'element': monElement,
                  }
        return render(request, self.template_name, context)

    def post(self, request, nomUrl):
        monElement = self.get_object(nomUrl)
        bound_form = self.form_class(
                                     request.POST,
                                     instance=monElement
                                    )
        if bound_form.is_valid():
            new_element = bound_form.save()
            return redirect(new_element)
        else:
            context = {
                       'form': bound_form,
                       'element': monElement,
                      }
        return render(
                      request,
                      self.template_name,
                      context
                     )

class ElementDialogueDelete(View):
    def get(self, request, nomUrl):
        monElement = get_object_or_404(
                                       ElementDialogue,
                                       nom = nomUrl
                                   )
        return render(request,
                      'dialogue/element_confirm_delete.html',
                      {'element': monElement}
                     )

    def post(self, request, nomUrl):
        monElement = get_object_or_404(
                                       ElementDialogue,
                                       nom = nomUrl
                                   )
        monElement.delete()
        return redirect('dialogue_liste')

def purgeElements(request):
    tableauDeLignes = []
    tableauDeLignes.append("Cette page radioactive est vouée à détruire les éléments de dialogue.")

    mesElements = ElementDialogue.objects.all()
    nbElements = ElementDialogue.objects.count()
    tableauDeLignes.append("J'ai compté %d éléments." % (nbElements))
    for numElement in range(nbElements - 1, -1, -1):
        monElement = mesElements[numElement]
        monNom = monElement.nom
        monParam1 = monElement.param1
        monParam2 = monElement.param2
        monParam3 = monElement.param3
        ligneAEcrire = "%d - [%s] - [%s] - [%s] - [%s]\n" % \
            (numElement, monNom, monParam1, monParam2, monParam3)
        tableauDeLignes.append(ligneAEcrire)
        # Il m'est arrivé de neutraliser la ligne qui suit, par prudence
        monElement.delete()

    template = loader.get_template('cestmoilechef/petite_merdasse.html')
    context = Context({ 'tabDeLignes': tableauDeLignes })
    output = template.render(context)
    return HttpResponse(output)

def formulaireAvecPost(request):
    template = loader.get_template('dialogue/formulaire_avec_post.html')
    context = Context({})
    output = template.render(context)
    return HttpResponse(output)

def importeElements(request):
    tableauDeLignes = []
    tableauDeLignes.append("Cette page est vouée à permettre l'importation des éléments de dialogue.")

    monFichier = Fichier("elements_dialogue.csv", False)
    while monFichier.index < monFichier.longueur:
        ligneLue = monFichier.litUneLigne()
        tableauDeLignes.append(ligneLue)
        mesBazars = ligneLue.split(',')
        monNom = vireGuill(mesBazars[0])
        monParam1 = vireGuill(mesBazars[1])
        monParam2 = vireGuill(mesBazars[2])
        monParam3 = vireGuill(mesBazars[3])
        tableauDeLignes.append("[%s] - [%s], [%s], [%s]" % (monNom, monParam1, monParam2, monParam3))
        # Il m'est arrive de neutraliser la ligne suivante pour éviter les
        # fausses manoeuvres, mais on en a quand même besoin
        ElementDialogue.objects.create(nom=monNom, param1=monParam1, param2=monParam2, param3=monParam3)
    monFichier.close()

    tableauDeLignes.append("En principe, si vous lisez ça, c'est que l'importation a eu lieu.")

    template = loader.get_template('cestmoilechef/petite_merdasse.html')
    context = Context({ 'tabDeLignes': tableauDeLignes })
    output = template.render(context)
    return HttpResponse(output)

def exporteElements(request):
    tableauDeLignes = []
    tableauDeLignes.append("Cette page est vouée à permettre l'export des éléments de dialogue.")

    monFichier = Fichier("elements_dialogue_export.csv", True)
    mesElements = ElementDialogue.objects.all()
    nbElements = ElementDialogue.objects.count()
    for numElement in range(nbElements):
        monElement = mesElements[numElement]
        monNom = monElement.nom
        monParam1 = monElement.param1
        monParam2 = monElement.param2
        monParam3 = monElement.param3
        ligneAEcrire = '"%s","%s","%s","%s"' % (monNom, monParam1, monParam2, monParam3)
        monFichier.ecritUneLigne(ligneAEcrire)
        tableauDeLignes.append(ligneAEcrire)
    monFichier.close()

    tableauDeLignes.append("En principe, si vous lisez ça, c'est que l'export a eu lieu.")

    template = loader.get_template('cestmoilechef/petite_merdasse.html')
    context = Context({ 'tabDeLignes': tableauDeLignes })
    output = template.render(context)
    return HttpResponse(output)

def formulaireAvecPost(request):
    template = loader.get_template('dialogue/formulaire_avec_post.html')
    context = Context({})
    output = template.render(context)
    return HttpResponse(output)

@csrf_exempt # En théorie, c'est une brèche de sécurité; en pratique... ca depend
def urlMiminePost(request):
    monFullPath = request.path_info # Je n'en fais rien, mais ça serait possible
    monActeur = request.POST.get('acteur')
    monInexistant = request.POST.get('inexistant')
    template = loader.get_template('dialogue/url_mimine_avec_post.html')
    context = Context({ 'monFullPath': monFullPath, 'monActeur': monActeur, 'monInexistant': monInexistant, })
    output = template.render(context)
    return HttpResponse(output)
