# Info

Programma per raccogliere dati su un libro via ISBN ricevuto da Bluetooth (scansione tramite app smartphone o PDA dedicato)

## Preparazione del Bluetooth

Per prima cosa è necessario abbinare il telefono col PC

Sul PC bisogna prima preparare un servizio in ascolto (come root):

    sdptool add --channel=3 SP
    mknod -m 666 /dev/rfcomm0 c 216 0
    rfcomm watch /dev/rfcomm0 3 /sbin/agetty rfcomm0 115200 linux

Sul telefono apriamo una connessione Bluetooth verso il PC

Infine, apriamo sul PC un terminale in ascolto sulla porta seriale designata in precedenza

    screen /dev/rfcomm0 115200

Riceveremo nel terminale la string con l'ISBN inviato dall'app
    
## App sul telefono

Avviate l'app sul telefono e toccate *"Connetti"*; selezionate poi il PC. A questo punto sarà possibile acquisire un ISBN e infine inviare l'ISBN letto al PC.

L'app invierà via Bluetooth la stringa `ISBN_0000000000000` 

## Scraping da Amazon (sul PC)

Entrate nella directory col terminale e digitate

    source bin/activate

In questo modo entrerete nel virtualenv di Python da cui potrete invocare il comando di scrapy seguente:

    python main.py <isbn>

dove al posto di `<isbn>` è possibile inserire l'ISBN ricevuto opzionalmente; se eseguite il comando omettendo l'argomento, un prompt **[ISBN] >** comparirà, accettando ISBN da cercare, fino all'inserimento di *"stop"*; specificando l'argomento `<isbn>`, verrà eseguita una sola ricerca per tale ISBN e il programma terminerà.

In alternativa, potete usare solo lo spider tramite il comando

    scrapy crawl bookspider -a isbn=0000000000000

dove di seguito `isbn=` va inserito l'ISBN ricevuto dal telefono via Bluetooth

Lo script `main.py` crea un file *result.csv* (se non presente) e vi aggiunge i risultati ottenuti dallo spider; le lettere *sds* sono aggiunte prima della prima riga del file, contenente i nomi delle colonne.
