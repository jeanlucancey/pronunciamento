Les exos Django de Jean-Luc Ancey
=================================

Bon, je ne domine pas Django, mais pétard, je me soigne. A
priori, le code de référence pour ce projet (hum) Django se
trouve en local, sur ma machine de Rambouillet, et c'est ça
que j'uploade sur Github. Mais pour faire tourner ça chez
Alwaysdata, voici ce qu'il convient de faire:

* Dans suorganizer/settings.py

   * Il faut mettre DEBUG à True.

   * Il faut inscrire ['jlancey.alwaysdata.net', '185.31.40.87', 'localhost']
   dans ALLOWED_HOSTS.

* Dans suorganizer/urls.py
   
   * Nota: en fait, ce qui suit est supposé être déjà fait, mais je le note quand même.

   * Il faut ajouter from cestmoilechef.views import pronunciamento

   * Il faut ajouter url(r'^cestmoilechef/', pronunciamento),

Ce qui suit n'est qu'un mémento de la syntaxe Markdown, que je
confesse ne pas encore dominer vraiment.


Titre de niveau 1
=================

Titre de niveau 2
-----------------


Ceci est un paragraphe.

Ceci est
un autre paragraphe.

Voici un mot *important* (avec une étoile). Voici un mot _important_ (avec des traits de soulignement).

Voici un mot **super important** (avec deux étoiles). Voici un mot __ super important__ (avec des traits de soulignement).

Et voici du **gras _italique_**.

# Titre de niveau 1

## Titre de niveau 2

### Titre de niveau 3

* une puce

* une autre puce

* encore une puce

On en reparlera.

* Une puce

   * Une sous-puce

   * Une autre sous-puce

* Une autre puce

On en reparlera.

1. Et de un

   8. Alfa

   5. Bravo

   3. Charlie (notez qu'il n'y a pas à numéroter proprement)

2. Et de deux

   - et du détail non numéroté

   - et un autre détail non numéroté

3. Et de trois

> Ceci est un texte cité. Je le fais
> courir sur plusieurs lignes
> pour voir ce que ça devient
> 
> > Une réponse à la citation
> >
> > Je continue
> 
> Et je reprends la première citation.

Voici un code en C:

    int main() {
        print("Hello world!\n");
        return 0;
    }

La fonction `printf` affiche du texte.

Voici du ~~texte barré~~.

Rendez-vous sur le [Site d'Amarelia](http://www.amarelia.ch) pour tout apprendre.

![La conversion de Saint Paul](http://courteline.org/hotes/images_blog/conversion_saint_paul_le_caravage.jpg)

------------------

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3

Et voilà, c'est à peu près tout.

