# Importa il modulo per web spider
import scrapy

# La classe pincipale estende scrapy.Spider
class BookSpider(scrapy.Spider):
    # Alias per lo spider
    name = "main"
    # URL per iniziare lo scraping
    def start_requests(self):
        url = 'https://www.amazon.it/s/ref=nb_sb_ss_i_9_4?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=isbn+'
        isbn = getattr(self, 'isbn', None)
        if isbn is not None:
            url = url + isbn
        else:
            url = url + '9781118999875' # Linux Bible
        yield scrapy.Request(url, self.parse)

    # Callback da eseguire dopo la richiesta HTTP
    def parse(self, response):
        first_result_url = response.css("a.s-access-detail-page::attr(href)").extract_first()
        if first_result_url is not None:
            next_page = response.urljoin(first_result_url)
            yield scrapy.Request(next_page, callback=self.parse_result)
    
    # Callback da eseguire per secondo, dopo aver seguito il link in parse()
    def parse_result(self, response):
        book = {} # Salva info libro nel dizionario Python
        book['title'] = response.css("span.a-size-large::text").extract_first()
        book['year'] = response.css("h1.a-size-large span::text").extract()[2][2:]
        for item in response.css("div.content li"):
            first = item.css("li b::text").extract_first()
            second = item.css("li::text").extract_first()[1:]
            if first == 'Editore:':
                book['editor'] = second
            elif first == 'Collana:':
                book['coll'] = second
            elif first == 'ISBN-13:':
                book['isbn'] = second
            else:
                pass
        print('\n', "<>"*20)
        print(book) # Stampa info salvate
        print("<>"*20, '\n')
