# dockercompose_to_macm_DJANGO <br>
Dockercompose_to_macm_DJANGO è un'applicazione web sviluppata con il supporto del framework <b>Django</b>. Essa è capace di ottenere un oggetto MACM a partire da un qualsiasi docker compose. L'oggetto MACM viene ottenuto tramite l'utilizzo della libreria <b>macm.py</b> che importa la libreria <b>networkx.py</b> a cui fa riferimento <b>Digraph.py</b>. Digraph definisce quello che è un grafo orientato(quello che è appunto un MACM), quindi andiamo ad estendere la classe Digraph per definire Node ed Edge che apparteranno al MACM. Definiamo poi <b>dockercompose_WriteTo_macmFile</b> che con il supporto delle classi Node ed Edge definiscono il parser vero e proprio che dato in input il docker compose e gli attributi associati al grafo orientato creano l'oggetto MACM.
Oltre alla creazione di un oggetto MACM è possibile anche caricare un MACM precedentemente creato e personalizzarne i corrispettivi attributi dei relativi servizi rappresentati dai vari nodi.
Una volta ottenuto il MACM è possibile (oltre ad effettuare una successiva personalizzazione) effettuare: <br>
    -il download del MACM nel corrispettivo linguaggio Cypher come <b>application_name_timestamp.macm</b>. <br>
    -una query cypher per inviare a neo4j ed ottenere un'effettiva visualizzazione del MACM in quanto grafo
    -realizzazione delle corrispettive pipeline associate ai vari servizi (e invio a Jenkins tramite API WORK IN PROGRESS)

### Start App
1. Aprire il terminale in /path/to/dockercompose_to_macm
2. Eseguire il comando: python manage.py runserver
3. L'applicazione web è ora disponibile tramite corrispettiva interfaccia

### Web Interface
L'interfaccia web è raggiungibile presso localhost:8000/app <br>
<br>
![Immagine](https://user-images.githubusercontent.com/90553744/146794715-06e04540-7193-476b-b976-f4a0f9de4629.png)
<br>
Personalizzazione dei vari campi associati ai vari servizi
<br>
![Immagine](https://user-images.githubusercontent.com/90553744/146797139-a55d6870-2802-43b0-8b8a-5749f4424a94.png)
