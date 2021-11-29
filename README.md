# dockercompose_to_macm_DJANGO <br>
Dockercompose_to_macm_DJANGO è un'applicazione web sviluppata con il supporto del framework <b>Django</b>. Essa è capace di ottenere un oggetto MACM a partire da un qualsiasi docker compose. L'oggetto MACM viene ottenuto tramite l'utilizzo della libreria <b>macm.py</b> che importa la libreria <b>networkx.py</b> a cui fa riferimento <b>Digraph.py</b>. Digraph definisce quello che è un grafo orientato(quello che è appunto un MACM), quindi andiamo ad estendere la classe Digraph per definire Node ed Edge che apparteranno al MACM. Nella libreria macm.py implementiamo il metodo <b>dockercompose_WriteTo_macmFile</b> che con il supporto delle classi Node ed Edge definiscono il parser vero e proprio che dato in input il docker compose(ovvero il suo path) e gli attributi associati al grafo orientato(app_id e application_name) creano l'oggetto MACM come <b>application_name_timestamp.macm</b>

### Start App
1. Aprire il terminale in /path/to/dockercompose_to_macm
2. Eseguire il comando: python manage.py runserver
3. L'applicazione web è ora disponibile tramite corrispettiva interfaccia

### Web Interface
L'interfaccia web è raggiungibile presso localhost:8000/app <br>
<br>
![webinterface](https://user-images.githubusercontent.com/90553744/143860659-59b0d1b7-130a-42ba-9cab-3ca45583e22b.png)
