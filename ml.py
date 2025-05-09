import scrapy


class MlSpider(scrapy.Spider):
    name = "ml"
    #allowed_domains = ["lista.mercadolivre.com.br"]
    #start_urls = ["https://lista.mercadolivre.com.br/oculos-masculino"]

    allowed_domains = ["www.amazon.com.br"]
    start_urls = ["https://www.amazon.com.br/oculos-masculino/s?k=oculos+masculino"]


    def parse(self, response):
        pass
