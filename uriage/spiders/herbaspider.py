import scrapy
from scrapy import Request
import re
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.log import configure_logging


class HerbaSpider(scrapy.Spider):
    name = 'herba'
    allowed_domains = ['herba.lt']
    start_urls = ['https://www.herba.lt/uriage-dermatologine-kosmetika']

    def parse(self, response):

        item = {}
        # get every url of every product in a page.
        for product in response.xpath('//h4[@class="product-name"]'):
            product_url = product.xpath('a/@href').get() #product.xpath('a').attrib['href']

            #item["title"] = product.xpath('a/@title').get()#product.xpath('a/text()').get()
            #item["href"] = product_url #product.xpath('a').attrib['href']
            yield Request(product_url, callback=self.parse_product_page, meta={'item': item})


        # we now have product titles from the first page, let's scrape from another one

        next_page = response.xpath('//a[@class="button next i-next"]').attrib['href']
        if next_page:
            yield response.follow(next_page, callback=self.parse) # response.follow is basically scrapy.Request 
        
    def parse_product_page(self, response):
        
        item = response.meta['item']
        item['title'] = response.xpath('//div[@class="product-name"]/h1/text()').get() # title of the product, making sure it's the one we got url from.
        #item['href'] = response.request.url
        item['price'] = re.findall(r"\d+,\d+ €", response.xpath('//p[@class="special-price"][1]/span[2]/text()').get())[0]
        # we're only getting one part of the description, because others might vary
        # it's probably WISE to remove spaces and endlines when comparing it aswell.
        item['description'] = response.xpath('//div[@class="std tab-description"]/p[1]/text()').get() # + p[2] + p[3]
        
        # this solution would be for getting whole description, not working yet.
        #for paragraph in response.xpath('//div[@class="std tab-description"]'):
            #item['description'] += paragraph.xpath('text()').get()
        yield item


class GintarineSpider(scrapy.Spider):
    name = 'gintarine'
    allowed_domains = ['gintarine.lt']
    start_urls = ['https://www.gintarine.lt/search?adv=false&cid=0&mid=0&vid=0&q=URIAGE&sid=false&isc=true&orderBy=0']

    def parse(self, response):
        
        item = {}

        for product in response.xpath('//h2[@class="product-title no-reserved-height"]'):
            product_url = product.xpath('a/@href').get()
            yield Request('https://www.gintarine.lt' + product_url, callback=self.parse_product_page, meta={'item': item})

        next_page = response.xpath('//li[@class="next-page"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_product_page(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//strong[@itemprop="name"]/text()').get()
        unchanged_price = response.xpath('//div[@class="product-price discounted-price"]/span/text()').get() if len(response.xpath('//div[@class="non-discounted-price"]')) == 1 else \
                        response.xpath('//div[@class="prices"]/div[1]/span/text()').get()
        item['price'] = re.findall(r"\d+,\d+€", unchanged_price)[0]
        item['description'] = response.xpath('//div[@class="full-description"]/descendant::*/text()').get() # first only
        #for text in response.xpath('//div[@class="full-description"]/descendant::*/text()'):
            #description += text.get()
        #item['description'] = description
        yield item


class BenuSpider(scrapy.Spider):
    pass

class EuroVaistineSpider(scrapy.Spider):
    pass

#configure_logging()
#process = CrawlerProcess()
#process.crawl(HerbaSpider)
#process.crawl(GintarineSpider)
#d = process.join()
##d.addBoth(lambda _: reactor.stop())

#reactor.run()
# process.start()