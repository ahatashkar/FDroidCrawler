import scrapy
import os
import re
import datetime
from scrapy import signals
import matplotlib.pyplot as plt


class FDroid(scrapy.Spider):
    name = "fdroid"
    start_urls = [
        'https://f-droid.org/en/categories/connectivity/',
        'https://f-droid.org/en/categories/development/',
        'https://f-droid.org/en/categories/graphics/',
        'https://f-droid.org/en/categories/internet/',
        'https://f-droid.org/en/categories/money/',
        'https://f-droid.org/en/categories/multimedia/',
        'https://f-droid.org/en/categories/navigation/',
        'https://f-droid.org/en/categories/phone-sms/',
        'https://f-droid.org/en/categories/reading/',
        'https://f-droid.org/en/categories/science-education/',
        'https://f-droid.org/en/categories/security/',
        'https://f-droid.org/en/categories/sports-health/',
        'https://f-droid.org/en/categories/system/',
        'https://f-droid.org/en/categories/theming/',
        'https://f-droid.org/en/categories/time/',
        'https://f-droid.org/en/categories/writing/'
    ]
    download_timeout = 1000

    count_github = 0
    count_gitlab = 0
    count_bitbucket = 0
    count_other = 0

    years_list = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FDroid, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        return spider

    def parse(self, response):

        for app in response.css('a.package-header'):
            # link = "https://f-droid.org/" + app.xpath('@href').get()
            link = response.urljoin(app.css('::attr(href)').get())

            yield scrapy.Request(link, callback=self.parse_page)

    def parse_page(self, response):
        # global count_github, count_gitlab, count_bitbucket, count_other, years_list

        app_name = response.css('.package-name::text')[0].get()
        app_name = app_name.strip()

        date_list = response.css('.package-version-header::text').getall()
        release_date = ""
        for date in date_list:
            if "Added" in date:
                release_date = date
                break

        year = -1
        temp = re.split("\s", release_date)
        for item in temp:
            try:
                if datetime.datetime.strptime(item, '%Y-%m-%d'):
                    release_date = item
                    year = release_date.split('-')[0]
            except ValueError:
                continue

        source_code = ""
        for link in response.css('.package-link'):
            if link.css('a::text').get() == 'Source Code':
                source_code = link.css('a::attr(href)').get()

        if "github" in source_code:
            self.count_github = self.count_github + 1

        elif 'gitlab' in source_code:
            self.count_gitlab = self.count_gitlab + 1

        elif 'bitbucket' in source_code:
            self.count_bitbucket = self.count_bitbucket + 1

        else:
            self.count_other = self.count_other + 1

        if self.years_list.get(year) is not None:
            self.years_list[year] = self.years_list[year] + 1
        else:
            self.years_list[year] = 1

        yield {
            # 'name': app_name,
            # 'link': response.request.url,
            'source': source_code,
            # 'date': release_date
            'year': year,
        }
        # yield scrapy.Request(response.urljoin(source_code + "/archive/master.zip"), callback=self.save_project)

    def save_project(self, response):
        if not os.path.exists('Projects'):
            os.mkdir('Projects')

        name = response.url.split('/')[-3]
        with open("Projects/" + name, 'wb') as f:
            f.write(response.body)
            f.close()

    def spider_opened(self, spider):
        print('Opening {} spider'.format(spider.name))

    def spider_closed(self, spider):
        print('Closing {} spider'.format(spider.name))

        line1 = "Github: " + str(self.count_github)
        line2 = "Gitlab: " + str(self.count_gitlab)
        line3 = "Bitbucket: " + str(self.count_bitbucket)
        line4 = "Other: " + str(self.count_other)

        f = open("statistics.txt", "a")
        f.write(line1 +'\n'+ line2 +'\n'+ line3 + '\n'+ line4 + '\n\n')

        for item in self.years_list:
            f.write(item + ': ' + str(self.years_list.get(item)) + '\n')

        self.years_list = sorted(self.years_list.items(), key=lambda t: t[0])
        x, y = zip(*self.years_list)
        plt.plot(x,y)
        plt.show()

        f.close()

