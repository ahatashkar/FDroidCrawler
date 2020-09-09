import scrapy


class FDroid(scrapy.Spider):
    name = "fdroid"
    start_urls = ['https://f-droid.org/en/categories/graphics/']

    def parse(self, response):
        for app in response.css('a.package-header'):
            # link = "https://f-droid.org/" + app.xpath('@href').get()
            link = response.urljoin(app.css('::attr(href)').get())

            # yield {
            #     'link': link,
            # }

            yield scrapy.Request(link, callback=self.parse_page)

    def parse_page(self, response):
        for link in response.css('.package-link'):
            if link.css('a::text').get() == 'Source Code':
                source_code = response.urljoin(link.css('a::attr(href)').get())


        # source_code = response.urljoin(response.css('.package-link a::attr(href)')[4].get())

        yield {
            'link': response.request.url,
            'source': source_code
        }