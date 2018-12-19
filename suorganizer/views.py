from django.shortcuts import redirect


def redirect_root(request):
    return redirect('cestmoilechef_pronunciamento')
