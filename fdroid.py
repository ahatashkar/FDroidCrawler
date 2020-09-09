import scrapy
import os


class FDroid(scrapy.Spider):
    name = "fdroid"
    start_urls = ['https://f-droid.org/en/categories/graphics/']

    def parse(self, response):

        # app = response.css('a.package-header')
        # link = response.urljoin(app.css('::attr(href)').get())
        # yield scrapy.Request(link, callback=self.parse_page)

        for app in response.css('a.package-header'):
            # link = "https://f-droid.org/" + app.xpath('@href').get()
            link = response.urljoin(app.css('::attr(href)').get())

            yield scrapy.Request(link, callback=self.parse_page)

    def parse_page(self, response):
        source_code = ""
        for link in response.css('.package-link'):
            if link.css('a::text').get() == 'Source Code':
                source_code = link.css('a::attr(href)').get()

        if "github" in source_code:
            yield {
                'link': response.request.url,
                'source': source_code
            }
            yield scrapy.Request(response.urljoin(source_code + "/archive/master.zip"), callback=self.save_project)

    def save_project(self, response):
        if not os.path.exists('Projects'):
            os.mkdir('Projects')

        name = response.url.split('/')[-3]
        with open("Projects/" + name, 'wb') as f:
            f.write(response.body)
            f.close()

