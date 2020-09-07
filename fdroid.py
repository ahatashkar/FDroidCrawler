import scrapy


class FDroid(scrapy.Spider):
    name = "fdroid"
    start_urls = ['https://f-droid.org/en/categories/graphics/']

    def parse(self, response):
        for app in response.css('a.package-header'):
            yield {
                'link': "https://f-droid.org/" + app.xpath('@href').get(),
            }
