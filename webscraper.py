import requests
import scrapy
from bs4  import BeautifulSoup 

class NewsSpider(scrapy.Spider):
    name = 'news'


class Article(scrapy.Item):
    headline = scrapy.Field()
