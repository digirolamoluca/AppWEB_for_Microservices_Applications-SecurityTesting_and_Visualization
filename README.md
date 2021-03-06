# AppWEB_for_Microservices_Applications-SecurityTesting_and_Visualization <br>
AppWEB_for_Microservices_Applications-SecurityTesting_and_Visualization è un'applicazione Web sviluppata con il supporto del framework <b>Django</b>. Essa è capace di ottenere un oggetto MACM a partire da un qualsiasi Docker Compose. L'oggetto MACM viene ottenuto tramite l'utilizzo della libreria <b>macm.py</b> che importa la libreria <b>networkx.py</b> a cui fa riferimento <b>Digraph.py</b>. Digraph definisce quello che è un grafo orientato(quello che è appunto un MACM), quindi andando ad estendere la classe Digraph per definire Node ed Edge che apparteranno al MACM. Si definisce poi <b>dockercompose_WriteTo_macmFile</b> che con il supporto delle classi Node ed Edge definisce il parser vero e proprio che dato in input il Docker Compose e gli attributi associati al grafo orientato creano l'oggetto MACM.<br><br>
Oltre alla creazione di un oggetto MACM è possibile anche caricare un MACM precedentemente creato e personalizzarne i corrispettivi attributi dei relativi servizi rappresentati dai vari nodi.<br><br>
Una volta ottenuto il MACM è possibile (oltre ad effettuare una successiva personalizzazione) effettuare: <br>
    -il download del MACM nel corrispettivo linguaggio Query Cypher come <b>application_name_timestamp.macm</b>. <br>
    -effettuare query Cypher per inviare a Neo4j ed ottenere un'effettiva visualizzazione del MACM in quanto grafo <br>
    -realizzazione delle corrispettive pipeline associate ai vari servizi SaaS e invio a Jenkins tramite API

### Start App
1. Aprire il terminale in /path/to/dockercompose_to_macm
2. Eseguire il comando: python manage.py runserver
3. L'applicazione web è ora disponibile tramite corrispettiva interfaccia

### Web Interface
L'interfaccia web è raggiungibile presso localhost:8000/app <br>
<br>
![Immagine](https://user-images.githubusercontent.com/90553744/146794715-06e04540-7193-476b-b976-f4a0f9de4629.png)

### Workflow
![WORKFLOW - Copia](https://user-images.githubusercontent.com/90553744/158799827-16d63406-6211-4506-8d94-f55bd027432b.png)
### Flusso di esecuzione
https://user-images.githubusercontent.com/90553744/158803158-c77462bf-94a5-42c9-89a1-0580c08510e3.mp4
