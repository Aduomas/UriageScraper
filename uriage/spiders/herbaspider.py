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

        # get every url of every product in a page.
        #urlList = response.xpath('//h4[@class="product-name"]/a/@href').extract()
        #print(urlList)

        item = {}

        for product in response.xpath('//h4[@class="product-name"]'):
            product_url = product.xpath('a').attrib['href']

            item["title"] = product.xpath('a/text()').get()
            item["href"] = product_url #product.xpath('a').attrib['href']
            yield Request(product_url, callback=self.parse_product_page, meta={'item': item})


        # we now have product titles from the first page, let's scrape from another one

        # css approach
        # next_page = response.css('a.button.next.i-next').attrib['href']

        next_page = response.xpath('//a[@class="button next i-next"]').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        
    def parse_product_page(self, response):
        print(response.xpath('//div[@class="product-name"]/h1/text()').get())# is response.meta['item']['title'])
        item = response.meta['item']
        yield item




# XPATH
# //h4[@class="product-name"]

#/html/body/div[4]/div[2]/div/div[1]/div[2]/ul/li[1]/div/div[2]/h4/a

# CSS
# h4.product-name
