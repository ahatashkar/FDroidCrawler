import scrapy
import os
import re
import datetime


class FDroid(scrapy.Spider):
    name = "fdroid"
    start_urls = ['https://f-droid.org/en/categories/graphics/']
    download_timeout = 1000

    def parse(self, response):

        # app = response.css('a.package-header')
        # link = response.urljoin(app.css('::attr(href)').get())
        # yield scrapy.Request(link, callback=self.parse_page)

        for app in response.css('a.package-header'):
            # link = "https://f-droid.org/" + app.xpath('@href').get()
            link = response.urljoin(app.css('::attr(href)').get())

            yield scrapy.Request(link, callback=self.parse_page)

    def parse_page(self, response):

        app_name = response.css('.package-name::text')[0].get()
        app_name = app_name.strip()

        date_list = response.css('.package-version-header::text').getall()
        release_date = ""
        for date in date_list:
            if "Added" in date:
                release_date = date
                break

        temp = re.split("\s", release_date)
        for item in temp:
            try:
                if datetime.datetime.strptime(item, '%Y-%m-%d'):
                    release_date = item
            except ValueError:
                continue

        source_code = ""
        for link in response.css('.package-link'):
            if link.css('a::text').get() == 'Source Code':
                source_code = link.css('a::attr(href)').get()

        if "github" in source_code:
            yield {
                'name': app_name,
                # 'link': response.request.url,
                # 'source': source_code,
                'date': release_date
            }
            # yield scrapy.Request(response.urljoin(source_code + "/archive/master.zip"), callback=self.save_project)

    def save_project(self, response):
        if not os.path.exists('Projects'):
            os.mkdir('Projects')

        name = response.url.split('/')[-3]
        with open("Projects/" + name, 'wb') as f:
            f.write(response.body)
            f.close()

