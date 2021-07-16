import os

import scrapy
from scrapy import Request

from scraper.items import Link

max_pages = int(os.environ.get('MAX_PAGES', '100'))


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['news.ycombinator.com']

    def get_url(page):
        return f"https://news.ycombinator.com/news?p={page}"

    start_urls = [get_url(1)]

    def parse(self, response):
        for a in response.css('.storylink'):
            yield Link(
                title = a.css('::text').extract_first(),
                url = a.css('::attr(href)').extract_first()
            )

        current_page = response.meta.get('page', 1)
        if current_page < max_pages:
            next_page = current_page + 1
            yield Request(url=NewsSpider.get_url(next_page), meta={'page': next_page})