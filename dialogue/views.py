from os import system

from django.http import (Http404, HttpResponse)
from django.template import Context, loader
from django.shortcuts import (get_object_or_404, \
                              redirect, \
                              # render_to_response, \
                              render)
from django.views.generic import View # Pour faire des class-based views, voir p. 255

from jla_utils.utils import Fichier

from .models import ElementDialogue
from .forms import ElementDialogueForm

def accueilDialogue(request):
    template = loader.get_template('dialogue/accueil.html')
    message = "Je veux juste pouvoir noter quelques paramètres quelque part."
    context = Context({'message': message})
    output = template.render(context)
    return HttpResponse(output)

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
