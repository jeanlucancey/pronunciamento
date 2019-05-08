from django.http import (Http404, HttpResponse)
from django.template import Context, loader
from django.shortcuts import (get_object_or_404, \
                              redirect, \
                              # render_to_response, \
                              render)
from django.views.generic import View # Pour faire des class-based views, voir p. 255

from .models import Dvd
from .forms import DvdForm

def accueilDvd(request):
    template = loader.get_template('dvd/accueil.html')
    message = "Je veux pouvoir faire un peu de saisie pour mes DVD."
    context = Context({'message': message})
    output = template.render(context)
    return HttpResponse(output)

class DvdList(View):
    def get(self, request):
        return render(request, \
                      'dvd/liste.html', \
                      {'dvd_list': Dvd.objects.all()})

class DvdCreate(View):
    form_class = DvdForm
    template_name = 'dvd/dvd_form.html'

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

def dvdDetail(request, slugUrl):
    try:
        monDvd = Dvd.objects.get(slug__iexact = slugUrl)
    except Dvd.DoesNotExist:
        raise Http404
    template = loader.get_template('dvd/dvd_detail.html')
    context = Context({'dvd': monDvd})
    output = template.render(context)
    return HttpResponse(output)

class DvdUpdate(View):
    form_class = DvdForm
    model = Dvd
    template_name = 'dvd/dvd_form_update.html'

    def get_object(self, slugArg):
        return get_object_or_404(
                                 self.model,
                                 slug=slugArg
                                )

    def get(self, request, slugUrl):
        monElement = self.get_object(slugUrl)
        context = {
                   'form': self.form_class(instance=monElement),
                   'element': monElement,
                  }
        return render(request, self.template_name, context)

    def post(self, request, slugUrl):
        monDvd = self.get_object(slugUrl)
        bound_form = self.form_class(
                                     request.POST,
                                     instance=monDvd
                                    )
        if bound_form.is_valid():
            new_element = bound_form.save()
            return redirect(new_element)
        else:
            context = {
                       'form': bound_form,
                       'dvd': monDvd,
                      }
        return render(
                      request,
                      self.template_name,
                      context
                     )

class DvdDelete(View):
    def get(self, request, slugUrl):
        monElement = get_object_or_404(
                                       Dvd,
                                       slug = slugUrl
                                   )
        return render(request,
                      'dvd/dvd_confirm_delete.html',
                      {'element': monElement}
                     )

    def post(self, request, slugUrl):
        monElement = get_object_or_404(
                                       Dvd,
                                       slug = slugUrl
                                   )
        monElement.delete()
        return redirect('dvd_liste')

def purgeDvd(request):
    tableauDeLignes = []
    tableauDeLignes.append("Cette page radioactive est vouée à détruire les DVD.")

    mesDvd = Dvd.objects.all()
    nbDvd = Dvd.objects.count()
    tableauDeLignes.append("J'ai compté %d DVD." % (nbDvd))
    for numDvd in range(nbDvd - 1, -1, -1):
        monDvd = mesDvd[numDvd]
        monTitre = monDvd.titre
        ligneAEcrire = "%d - [%s]\n" % \
            (numDvd, monTitre)
        tableauDeLignes.append(ligneAEcrire)
        # Je neutralise la ligne qui suit, par prudence
        # monDvd.delete()

    template = loader.get_template('cestmoilechef/petite_merdasse.html')
    context = Context({ 'tabDeLignes': tableauDeLignes })
    output = template.render(context)
    return HttpResponse(output)
