import scrapy


class MlSpider(scrapy.Spider):
    name = "mercadolivre"
    #allowed_domains = ["lista.mercadolivre.com.br"]
    #start_urls = ["https://lista.mercadolivre.com.br/oculos-masculino"]

    allowed_domains = ["www.amazon.com.br"]
    start_urls = ["https://www.amazon.com.br/oculos-masculino/s?k=oculos+masculino"] #request get
    
      


    def parse(self, response): #parser q trabaLHA C A RESPOSTA DO GET
        products = response.css('div.a-section.a-spacing-base') #TODOS items

        for product in products:
            yield {
                'brand' : product.css('span.a-size-base-plus.a-color-base::text').get()
                #'title' : product.css('span.a-size-base-plus.a-color-base.a-text-normal::text').get(),
                #'price' : product.css('span.a-price-whole::text').get(),
                #'price' : product.css('span.a-price-symbol::text').get(),
                #'rating' : product.css('span.a-icon-alt::text').get(),
                #'reviews' : product.css('span.a-size-base.s-underline-text.s-underline-link-text.s-link-style::text').get(),
                
                
            }
        #next_page = response.css('a.s-pagination-next::attr(href)').get()
        #if next_page:
         #   yield response.follow(next_page, callback=self.parse)       
