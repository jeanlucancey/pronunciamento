#!/usr/bin/perl -w
use LWP::Simple;
system("./mon_traitement_long_en_C");
get("http://monUrlCompletePourDireADjangoQueCEstBonIlPeutYAller");
