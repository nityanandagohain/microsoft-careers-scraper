# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import re
import json

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    start_urls = ['https://careers.microsoft.com/us/en/search-results?from=0&s=1&rt=professional']
    ids = []
    from_ = 0
    def parse(self, response):
        data = response.css("script").extract_first()
        data = re.findall('"data":{"jobs.*',data)
        data = re.findall('.*,"aggregations', data[0])
        data = data[0].replace(',"aggregations',"")
        data = data.replace('"data":{"jobs":',"")
        data = json.loads(data)
        for d in data:
            # print(d['jobId'])
            if d['jobId'] not in self.ids:
                self.ids.append(d['jobId'])
                name = d['title'].replace(" ","-")
                url = "https://careers.microsoft.com/us/en/job/{}".format(d['jobId'])
                print(url)
                yield response.follow(url, callback=self.parse_job)
        if JobsSpider.from_ < (4340):
            JobsSpider.from_ += 40
            next_link = "https://careers.microsoft.com/us/en/search-results?from={}&s=1&rt=professional".format(self.from_)
            yield response.follow(next_link, callback=self.parse)

    def parse_job(self, response):
        data = response.css("script")[1].extract()
        data = re.findall('"data":{"job.*',data)
        data = re.sub(',"isMultiLocatio.*',"",data[0])
        data = re.sub('.*job":',"",data)
        data = json.loads(data)
        yield data