from os import system

from django.http import HttpResponse
from django.template import Context, loader

def viewSinodoju (request):
    tableauDeLignes = []
    tableauDeLignes.append("Cette page est la page de Sinodoju.")

    system("./sinodoju.pl > cr_perl.txt 2> cr2_perl.txt &")

    tableauDeLignes.append("En principe, si vous lisez ça, c'est que Sinodoju a eu lieu.")

    template = loader.get_template('cestmoilechef/petite_merdasse.html')
    context = Context({ 'tabDeLignes': tableauDeLignes })
    output = template.render(context)
    return HttpResponse(output)
