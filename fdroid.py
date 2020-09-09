import scrapy


class FDroid(scrapy.Spider):
    name = "fdroid"
    start_urls = ['https://f-droid.org/en/categories/graphics/']

    def parse(self, response):

        app = response.css('a.package-header')
        link = response.urljoin(app.css('::attr(href)').get())
        yield scrapy.Request(link, callback=self.parse_page)

        # for app in response.css('a.package-header'):
        #     # link = "https://f-droid.org/" + app.xpath('@href').get()
        #     link = response.urljoin(app.css('::attr(href)').get())
        #
        #     yield scrapy.Request(link, callback=self.parse_page)

    def parse_page(self, response):
        source_code = ""
        for link in response.css('.package-link'):
            if link.css('a::text').get() == 'Source Code':
                source_code = link.css('a::attr(href)').get()

        yield {
            'link': response.request.url,
            'source': source_code
        }

        item = ZipfilesItem()
        item['file_urls'] = [response.urljoin(source_code + "/archive/master.zip")]
        yield item

        # yield scrapy.Request(response.urljoin(source_code + "/archive/master.zip"), callback=self.save_project)

    def save_project(self, response):
        path = response.url
        with open(path, 'wb') as f:
            f.write(response.body)


class ZipfilesItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field