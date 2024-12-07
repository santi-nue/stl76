import scrapy
from scrapy.crawler import CrawlerProcess

class ImageSpider(scrapy.Spider):
    name = 'image_spider'
    start_urls = ['http://www.spanishbeercoasters.es']

    def parse(self, response):
        # Extract image URLs
        image_urls = response.css('img::attr(src)').getall()
        for image_url in image_urls:
            yield {'image_url': response.urljoin(image_url)}
        
        # Follow links to subdirectories
        for next_page in response.css('a::attr(href)').getall():
            yield response.follow(next_page, self.parse)

def main():
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'images.json',
        'LOG_LEVEL': 'ERROR',  # Reduce log output
    })
    
    process.crawl(ImageSpider)
    process.start()  # The script will block here until the crawling is finished

if __name__ == '__main__':
    main()
