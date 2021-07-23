import scrapy
from scrapy import Request


class HerbaSpider(scrapy.Spider):
    name = 'herba'
    allowed_domains = ['herba.lt']
    start_urls = ['https://www.herba.lt/uriage-dermatologine-kosmetika']

    def parse(self, response):

        # css approach
        # for product in response.css('h4.product-name'):
        #     yield {
        #         "text": product.css('a::text').get()
        #     }

        item = {}
        # get every url of every product in a page.
        for product in response.xpath('//h4[@class="product-name"]'):
            product_url = product.xpath('a/@href').get() #product.xpath('a').attrib['href']

            #item["title"] = product.xpath('a/@title').get()#product.xpath('a/text()').get()
            #item["href"] = product_url #product.xpath('a').attrib['href']
            yield Request(product_url, callback=self.parse_product_page, meta={'item': item})


        # we now have product titles from the first page, let's scrape from another one

        # css approach: response.css('a.button.next.i-next').attrib['href']

        next_page = response.xpath('//a[@class="button next i-next"]').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse) # response.follow is basically scrapy.Request 
        
    def parse_product_page(self, response):
        
        item = response.meta['item']
        item['title'] = response.xpath('//div[@class="product-name"]/h1/text()').get() # title of the product, making sure it's the one we got url from.
        item['href'] = response.request.url

        # we're only getting one part of the description, because others might vary
        # it's probably WISE to remove spaces and endlines when comparing it aswell.
        item['description'] = response.xpath('//div[@class="std tab-description"]/p[1]/text()').get()
        
        # this solution would be for getting whole description, not working yet.
        #for paragraph in response.xpath('//div[@class="std tab-description"]'):
            #item['description'] += paragraph.xpath('text()').get()
        yield item


class GintarineSpider(scrapy.Spider):
    name = 'gintarine'
    allowed_domains = ['gintarine.lt']
    start_urls = ['https://www.gintarine.lt/search?adv=false&cid=0&mid=0&vid=0&q=URIAGE&sid=false&isc=true&orderBy=0']

    def parse(self, response):
        pass

    def parse_product_page(self, response):
        pass