import scrapy


class HerbaSpider(scrapy.Spider):
    name = 'herba'
    start_urls = ['https://www.herba.lt/uriage-dermatologine-kosmetika']

    def parse(self, response):

        # css approach
        # for product in response.css('h4.product-name'):
        #     yield {
        #         "text": product.css('a::text').get()
        #     }

        for product in response.xpath('//h4[@class="product-name"]'):
            yield {
                "text": product.xpath('a/text()').extract(),
                "href": product.xpath('a').attrib['href'],
            }

        # we now have product titles from the first page, let's scrape from another one

        # css approach
        # next_page = response.css('a.button.next.i-next').attrib['href']

        next_page = response.xpath('//a[@class="button next i-next"]').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        




# XPATH
# //h4[@class="product-name"]

#/html/body/div[4]/div[2]/div/div[1]/div[2]/ul/li[1]/div/div[2]/h4/a

# CSS
# h4.product-name
