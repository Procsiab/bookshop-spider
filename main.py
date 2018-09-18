#!/usr/bin/python3

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals

# Importa la classe dello spider BookSpider
import sys
import os
sys.path.append(os.path.abspath("/home/l3r0/Documenti/py_stuff/bookshop_spider/bookshop_spider/spiders"))
from bookspider import BookSpider

import csv

# Variabile globale per l'ISBN ricevuto
ISBN_RECEIVED = None
# Nome del file che conterrà i risultati
RESULT_FILE_NAME = "result.csv"

# Aggiunge al file CSV i risultati ottenuti da Amazon.it
def append_dic_csv(dic):
    with open(RESULT_FILE_NAME, 'a') as f:
        w = csv.DictWriter(f, dic.keys())
        w.writerow(dic)
    print("Informazioni aggiunto al file result.csv")

# Inizializza il file che conterrà i dati CSV ottenuti dallo spider
def create_csv(dic):
    try:
        with open(RESULT_FILE_NAME, 'r') as f:
            print("Trovato file result.csv")
    except FileNotFoundError:
        print("Creo file result.csv")
        with open(RESULT_FILE_NAME, 'w') as f:
            w = csv.DictWriter(f, dic.keys())
            w.writeheader()

# Helper per rimuovere la punteggiatura riservata dalle stringhe che andranno nel file CSV
def csvfy(string):
    s = string
    if s is not None and type(s) == str:
        for ch in [', ','; ',',',';']:
            if ch in s:
                s = s.replace(ch, " ")
    return s

# Funzione chiamata subito prima della chiusura dello spider
def close_spider(spider, reason):
    print("Ricerca terminata per l'ISBN ricevuto:")
    for key, value in spider.result.items():
        spider.result[key] = csvfy(value)
        print("  {0}: {1}".format(key, value))
    # Creo il file per salvare i risultati, se non presente
    create_csv(spider.result)
    # Aggiungo una nuova riga coi risultati al file
    append_dic_csv(spider.result)

# Funzione eseguita all'avvio dello script
def main():
    mySpider = BookSpider()
    process = CrawlerProcess(get_project_settings())
    crawler = process.create_crawler(mySpider)

    # Connetti la funzione close_spider al segnale spider_closed
    crawler.signals.connect(close_spider, signals.spider_closed)
    # Avvia il processo assegnato allo spider m
    process.crawl(crawler, isbn=ISBN_RECEIVED)
    process.start()

if __name__ == '__main__':
    # Usa il primo argomento da riga di comando come ISBN ricevuto
    if len(sys.argv) > 1 and sys.argv[1] is not None:
        ISBN_RECEIVED = sys.argv[1]
    main()
