#!/usr/bin/python3
# -*- coding: utf_8 -*

import scrapy
import logging


# La classe pincipale estende scrapy.Spider
class BookSpider(scrapy.Spider):
    # Alias per lo spider
    name = "bookspider"
    # Disablita logging dello spider
    custom_settings = {'LOG_ENABLED': False}
    # Disabilita logging di scrapy
    logging.getLogger('scrapy').propagate = False
    # Dizionario per salvare i dati otenuti
    result = {}

    # URL per iniziare lo scraping, riceve ISBN come argomento -a
    def start_requests(self):
        url = 'https://www.amazon.it/s/ref=nb_sb_ss_i_9_4?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=isbn+'
        isbn = getattr(self, 'isbn', None)
        if isbn is not None:
            url = url + isbn
        else:
            url = url + '9788808220851'
        yield scrapy.Request(url, self.parse)

    # Callback da eseguire dopo la richiesta HTTP
    def parse(self, response):
        first_result_url = response.css("a.a-link-normal.a-text-normal::attr(href)").extract_first()
        if first_result_url is not None:
            next_page = response.urljoin(first_result_url)
            yield scrapy.Request(next_page, callback=self.parse_result)

    # Callback da eseguire per secondo, dopo aver seguito il link in parse()
    def parse_result(self, response):
        book = {'titolo': None, 'anno': None, 'editore': None, 'collana': None, 'isbn': None} # Salva info libro nel dizionario Python
        book['titolo'] = response.css("span.a-size-large::text").extract_first()
        book['anno'] = response.css("h1.a-size-large span::text").extract()[2][2:]
        # Cerca dati nella descrizione prodotto
        for item in response.css("div.content li"):
            first = item.css("li b::text").extract_first()
            second = item.css("li::text").extract_first()[1:]
            if first == 'Editore:':
                book['editore'] = second
            elif first == 'Collana:':
                book['collana'] = second
            elif first == 'ISBN-13:':
                book['isbn'] = second
            else:
                pass
        self.result = book  # Salva le informazioni nella variabile di istanza
