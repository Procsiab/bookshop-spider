from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals

# Importa la classe dello spider BookSpider
import sys
import os
sys.path.append(os.path.abspath("/home/l3r0/Documenti/py_stuff/bookshop_spider/bookshop_spider/spiders"))
from bookspider import BookSpider

# Variabile globale per l'ISBN ricevuto
ISBN_RECEIVED = "9788808220851"

# Funzione chiamata subito prima della chiusura dello spider
def close_spider(spider, reason):
    print("Ricerca terminata per l'ISBN ricevuto:")
    for key, value in spider.result.items():
        print("  {0}: {1}".format(key, value))

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
   main()
