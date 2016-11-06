import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from lyric_crawler.items import AlbumLyricItem

class LyricsSpider(CrawlSpider):
    name = 'lyrics_spider'
    allowed_domains = ['darklyrics.com']
    start_urls = ['http://www.darklyrics.com']

    rules = (
        # Follow links (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=(r'.*www\.darklyrics\.com\/\w\.html'))),
        Rule(LinkExtractor(allow=(r'.*www\.darklyrics\.com\/\w\/\w+\.html'))),
        Rule(LinkExtractor(allow=(r'.*www\.darklyrics\.com\/lyrics\/\w+\/\w+\.html')), callback='parse_album'),
    )

    def extract_latest(self, links):
        for link in links:
            link.url = re.sub(r'/web/.*/','/web/',link.url)
        return links

    def parse_album(self, response):
        url = response.url.split('/')
        item = AlbumLyricItem()
        item['album'] = url[-1].split('.')[0]
        item['artist'] = url[-2]
        item['lyrics'] = "".join(response.css('.lyrics::text').extract()).replace('\n', ' ').replace('\r',' ').strip()
        yield item
