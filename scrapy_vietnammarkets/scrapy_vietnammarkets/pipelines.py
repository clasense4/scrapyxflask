# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
import datetime
import os

class CompanyProfilePipeline(object):
    def open_spider(self, spider):
        self.path = os.getcwd() + '/../webserver/'
        self.name = 'company_profile.json'
        self.jsons = []
        try:
            os.remove(self.path + self.name)
        except OSError:
            pass

    def close_spider(self, spider):
        time.sleep(1)
        json_data = json.dumps(self.jsons, ensure_ascii=False, indent=4)

        files = open(self.path + self.name, 'w+')
        files.write(json_data)
        files.close()

    def process_item(self, item, spider):
        self.jsons.append(item)
        return item

class CompanyIndexPipeline(object):
    def open_spider(self, spider):
        self.path = os.getcwd() + '/../webserver/'
        self.name = 'company_index.json'
        self.jsons = []
        try:
            os.remove(self.path + self.name)
        except OSError:
            pass

    def close_spider(self, spider):
        time.sleep(1)
        json_data = json.dumps(self.jsons, ensure_ascii=False, indent=4)

        files = open(self.path + self.name, 'w+')
        files.write(json_data)
        files.close()

    def process_item(self, item, spider):
        company_index = item.copy()

        dropped_keys = [
            'address', 'phone', 'auditing_company', 'business_summary', 'business_registration',
            'email', 'website', 'description', 'country', 'financial_summary', 'revenue'
        ]
        for key in dropped_keys:
            company_index.pop(key, None)
            company_index['crawled_at'] = str(datetime.datetime.now())

        self.jsons.append(company_index)
        return item
