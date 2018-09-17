# Info

Programma per raccogliere dati su un libro via ISBN ricevuto da bluetooth (scansione tramite app smartphone o PDA dedicato)

## Preparazione del Bluetooth

Per prima cosa è necessario abbinare il telefono col PC

Sul PC bisogna prima preparare un servizio in ascolcto (come root):

    sdptool add --channel=3 SP
    mknod -m 666 /dev/rfcomm0 c 216 0
    rfcomm watch /dev/rfcomm0 3 /sbin/agetty rfcomm0 115200 linux

Sul telefono apriamo una connessione bluetooth verso il PC

Infine, apriamo sul PC un terminale in ascolto sulla porta seriale designata in precedenza

    screen /dev/rfcomm0 115200 
    
## App sul telefono

Avviate l'app sul telefono e toccate *"Connetti"*; selezionate poi il PC. A questo punto sarà possibile acquisire un ISBN e infine inviare l'ISBN letto al PC.

L'app invierà via Bluetooth la stringa `ISBN_0000000000000` 

## Scraping da Amazon

Entrate nella directory col terminale e digitate

    source bin/activate

In questo modo entrerete nel virtualenv di Python da cui potrete invocare il comando di scrapy seguente:

    scrapy crawl bookspider -a isbn=0000000000000

dove a seguire `isbn=` va inserito l'ISBN ricevuto dal telefono via bluetooth