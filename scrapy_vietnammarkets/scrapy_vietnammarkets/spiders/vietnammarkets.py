# -*- coding: utf-8 -*-
import scrapy
from w3lib.html import remove_tags

class VietnammarketsSpider(scrapy.Spider):
    name = 'vietnammarkets'
    allowed_domains = ['vietnammarkets.com']
    start_urls = ['http://stock.vietnammarkets.com/vietnam-stock-market.php']
    jsons = []
    json = {}

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_main)

    def parse_main(self, response):
        tr = response.xpath('//*[@id="VNMC_contentinner"]//table//tr[position()>1]')
        # print(tr.extract())
        for tds in tr:
            td = tds.xpath('td')
        # for i in range(0, 5) :
        #     td = tr[i].xpath('td')

            company_url = td.xpath('a/@href').extract()[0]

            self.json["name"] = td.xpath('text()').extract()[0]
            self.json["url"] = company_url
            self.json["ticker_symbol"] = td.xpath('a/text()').extract()[0]
            self.json["country"] = "Vietnam"
            self.json["business"] = td.xpath('text()').extract()[1]
            self.json["listing_bourse"] = td.xpath('text()').extract()[2]
            position = len(self.jsons)
            self.jsons.append(self.json)
            self.json = {}

            yield scrapy.Request(company_url, callback=self.parse_company_page, meta = {'position' : position})

    def parse_company_page(self, response):
        position = response.meta['position']
        td = response.xpath('//div[@class="results"]/table[1]/tr/td')

        # Extract Company
        company_profile = remove_tags(td[0].extract()).split('\n\t\t\t\t\t\t')
        self.jsons[position]["address"] = ', '.join(self.cleanStrings(company_profile[2].split(',')))
        # Phone number
        if self.hasNumbers(company_profile[3]) and self.hasNumbers(company_profile[4]):
            self.jsons[position]["phone"] = [ company_profile[3].strip(), company_profile[4].strip() ]
        elif self.hasNumbers(company_profile[3]):
            self.jsons[position]["phone"] = company_profile[3].strip()
        elif self.hasNumbers(company_profile[4]):
            self.jsons[position]["phone"] = company_profile[4].strip()
        else:
            self.jsons[position]["phone"] = ''
        self.jsons[position]["email"] = company_profile[5].strip()
        self.jsons[position]["website"] = company_profile[6].strip()

        business_summary = remove_tags(td[2].extract()).split('\n\t\t\t\t\t\t')
        self.jsons[position]["description"] = business_summary[2]
        self.jsons[position]["auditing_company"] = business_summary[4]

        auditing_company = td[2].extract().split('<br>')
        auditing_company = self.cleanStrings(auditing_company)
        auditing_company = self.cleanHtml(auditing_company)
        del auditing_company[0]
        del auditing_company[-1]

        self.jsons[position]["auditing_company"] = ''
        self.jsons[position]["business_registration"] = {}

        auditing_company_index = auditing_company.index('Auditing Company:')
        business_registration_index = auditing_company.index('Business Registration:')

        for i in range(len(auditing_company)):
            if auditing_company[i]:
                if i > auditing_company_index and i < business_registration_index:
                    # self.jsons[position]["auditing_company"].append(auditing_company[i])
                    self.jsons[position]["auditing_company"] += " " + auditing_company[i]
                elif i > business_registration_index:
                    if 'Established' in auditing_company[i]:
                        self.jsons[position]['business_registration']['established_license'] = auditing_company[i].split(':')[1].strip()
                    elif 'Business' in auditing_company[i]:
                        self.jsons[position]['business_registration']['business_license'] = auditing_company[i].split(':')[1].strip()

        # Financial Summary
        financial_summary = remove_tags(td[1].extract()).split('\n\t\t\t\t\t\t\t')
        self.jsons[position]['revenue'] = self.toNumber(financial_summary[3].split(':')[1])
        self.jsons[position]['financial_summary'] = {}
        self.jsons[position]['financial_summary']['capital_currency'] = financial_summary[2].split(':')[1]
        self.jsons[position]['financial_summary']['market_cap'] = self.toNumber(financial_summary[3].split(':')[1])
        self.jsons[position]['financial_summary']['par_value'] = self.toNumber(financial_summary[4].split(':')[1])
        self.jsons[position]['financial_summary']['equity'] = self.toNumber(financial_summary[5].split(':')[1])
        self.jsons[position]['financial_summary']['listing_volume'] = self.toNumber(financial_summary[6].split(':')[1])
        self.jsons[position]['financial_summary']['listed_date'] = financial_summary[7].split(':')[1]
        self.jsons[position]['financial_summary']['initial_listed_price'] = self.toNumber(financial_summary[8].split(':')[1])

        return self.jsons[position]

    def hasNumbers(self, string):
        return any(char.isdigit() for char in string)

    def cleanStrings(self, strings):
        return [string.strip() for string in strings]

    def cleanHtml(self, strings):
        return [remove_tags(string) for string in strings]

    def toNumber(self, string):
        return int(float(string.replace(',','')))