import scrapy
from urllib.parse import urljoin

class MlSpider(scrapy.Spider):
    name = "mercadolivre"
    #allowed_domains = ["lista.mercadolivre.com.br"]
    #start_urls = ["https://lista.mercadolivre.com.br/oculos-masculino"]

    allowed_domains = ["www.amazon.com.br"]
    start_urls = ["https://www.amazon.com.br/oculos-masculino/s?k=oculos+masculino"] #request get
    
    page_count = 1
    max_pages = 5  


    def parse(self, response): #parser q trabaLHA C A RESPOSTA DO GET
        products = response.css('div.a-section.a-spacing-base') #TODOS items

        for product in products:
            #prices = product.css('span.a-price-fraction::text').getall()
            #cents = product.css('span.a-price-cents::text').getall()
            yield {
                'brand' : product.css('span.a-size-base-plus.a-color-base::text').get(),
                'price' : product.css('span.a-price-whole::text').get(),
                #'old_price_reais' : prices[0] if len(prices) > 0 else None,
                #'old_price_cents' : cents[0] if len(prices) > 0 else None,
                #'new_price_reais' : prices[1] if len(prices) > 1 else None,
                #'new_price_cents' : cents[1] if len(prices) > 1 else None,
                'rating' : product.css('span.a-size-base.s-underline-text::text').get(),
                'title' : product.css('h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal::text').get()
                
                
            }

        if self.page_count < self.max_pages:
            # Select the 'href' from the next page button
            next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button::attr(href)').get()
            
            if next_page:
                self.page_count += 1
                # Construct the absolute URL
                next_page_url = urljoin(response.url, next_page)
                self.logger.info(f"Following next page: {next_page_url}")
                
                yield scrapy.Request(
                    url=next_page_url,
                    callback=self.parse
                )
            else:
                self.logger.info("No next page found.")
        
         #   yield response.follow(next_page, callback=self.parse)       
 