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

- Le type de composant qui se trouve a l'autre bout

  .. code-block:: javascript
     {
       'service': 'node'
     }

- La version du composant et de son API

  .. code-block:: javascript
     {
       'version': '0.0.1',
       'api_version': '0.1.1'
     }

- Les capacites du composant
  Ce sont les fonctionalites disponible pour ce composant, par exemple
  un node n'est pas forcement capable de deployer un LB ou une instance.

  Cela offre par ailleurs la possibilite de desactiver des features.

  .. code-block:: javascript
     {
       'capabilities': [
         'lb',
	 'instance'
       ]
     }

Ce qui donne au final:

  .. code-block:: javascript
     {
       'service': 'node',
       'version': '0.0.1',
       'api_version': '0.1.1'
       'capabilities': [
         'lb',
         'instance'
       ]
     }

