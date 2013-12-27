Pistes de reflexions pour l'implementation des API
==================================================

Abstract
--------

Ce README a pour but de fournir des pistes de reflexions concernant
l'implementation des API orchester.io.

Le but n'est pas de documenter la structure exacte des API pour le
moment mais de definir les grandes lignes.


Root URL
--------

L'url '/' devrait fournir (pour l'ensemble des composants), les
informations suivantes:

- Le type de composant qui se trouve a l'autre bout::

    {
        'service': 'node'
    }


- La version du composant et de son API::

    {
      'version': '0.0.1',
      'api_version': '0.1.1'
    }

- Les capacites du composant
  Ce sont les fonctionalites disponible pour ce composant, par exemple
  un node n'est pas forcement capable de deployer un LB ou une instance.

  Cela offre par ailleurs la possibilite de desactiver des features.::

     {
       'capabilities': [
         'lb',
	 'instance'
       ]
     }

Ce qui donne au final::

     {
       'service': 'node',
       'version': '0.0.1',
       'api_version': '0.1.1'
       'capabilities': [
         'lb',
         'instance'
       ]
     }


IDs vs. URLS
------------

Les bons guides de design d'API recommandent l'utilisation d'urls plutot que
d'id dans les retours des API dans la mesure ou cela facilite l'implementation
des clients qui n'ont pas alors a connaitre les urls. 

Ce qui donne des trucs du style::

    {
       'workers': [
         'https://node-1.orchester.io/v1/worker/1',
         'https://node-1.orchester.io/v1/worker/42'
       ]
    }


Plutot que::

    {
       'workers': [
         1,
         42
       ]
    }


HTTP methods
------------

On se limitera aux methodes HTTP suivantes:

- `GET`
- `POST`: Pour la creation d'objets
- `PUT`: Pour la mise a jour d'objets
- `DELETE`: Pour la suppression d'objets

