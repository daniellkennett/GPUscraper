import scrapy


class RedditSpider(scrapy.Spider):
    name = 'BestBuy'
    start_urls = ['https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=chipsetmanufacture_facet%3DChipset%20Manufacture~NVIDIA']

    def parse(self, response):
        for products in response.css('div.product-item-info'):
            yield{
                'name': products.css('a.product-items')
                'price':
                'link':
            }

        for link in links:
            url = link.get()

