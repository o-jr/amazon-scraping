import scrapy
import random
from urllib.parse import urljoin
from scrapy.exceptions import IgnoreRequest


USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.3',
    # Add more User-Agents here
]

class MlSpider(scrapy.Spider):
    name = "amazon"

    allowed_domains = ["www.amazon.com.br"]
    start_urls = ["https://www.amazon.com.br/oculos-masculino/s?k=oculos+masculino"] #request get
    
    page_count = 1
    max_pages = 8 # Define the maximum number of pages to scrape  

    def start_requests(self):
            for url in self.start_urls:
                yield scrapy.Request(url, headers={'User-Agent': random.choice(USER_AGENT_LIST)}, callback=self.parse)
                
    def parse(self, response): # callback function parser q trabaLHA C A RESPOSTA DO GET
        if response.status == 503:
            self.logger.info("Received 503 status, retrying after delay.")
            # You can use scrapy's built-in retry mechanism or custom logic
            raise IgnoreRequest("Received 503 status, retrying after delay.")
        
        self.logger.info(f"Parsing page {self.page_count}: {response.url}")
        products = response.css('div.a-section.a-spacing-base') # # Select the product containers of all itemns

        # for product in products:
        #     #prices = product.css('span.a-price-fraction::text').getall()
        #     #cents = product.css('span.a-price-cents::text').getall()
        #     yield {
        #         'brand' : product.css('span.a-size-base-plus.a-color-base::text').get(),
        #         'price' : product.css('span.a-price-whole::text').get(),
        #         'rating' : product.css('span.a-size-base.s-underline-text::text').get(),
        #         'title' : product.xpath('//div//a//h2//span/text()').get() #  = response.css('div a h2 span::text').getall()
                
                #'old_price_reais' : prices[0] if len(prices) > 0 else None,
                #'old_price_cents' : cents[0] if len(prices) > 0 else None,
                #'new_price_reais' : prices[1] if len(prices) > 1 else None,
                #'new_price_cents' : cents[1] if len(prices) > 1 else None,
             
                
            #}
        for product in products:
            yield {
            'brand': product.css('span.a-size-base-plus.a-color-base::text').get(),
            'price': product.css('span.a-price-whole::text').get(),
            'rating': product.css('span.a-size-base.s-underline-text::text').get(),
            #'title': product.css('h2 a span::text').get(),
            'title': product.xpath('.//div//a//h2//span/text()').get(),
            'page': self.page_count
            }
             

        if self.page_count < self.max_pages:
            next_page = next_page = response.css('a.s-pagination-next::attr(href)').get()
            #next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button::attr(href)').get() # Select the 'href' from the next page button
            
            if next_page:
                self.page_count += 1
                # Construct the absolute URL
                next_page_url = urljoin(response.url, next_page) 
                self.logger.info(f"Following next page: {next_page_url}")
                
                yield scrapy.Request(# request to the next page
                    #method='GET',
                    url=next_page_url,
                    callback=self.parse
                )
            else:
                self.logger.info("No next page found.")
        
         #   yield response.follow(next_page, callback=self.parse)       
 