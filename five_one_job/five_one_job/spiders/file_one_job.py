# -*- coding: utf-8 -*-
import scrapy
from five_one_job.items import FiveOneJobItem
import re


class FileOneJobSpider(scrapy.Spider):
    name = 'file_one_job'
    allowed_domains = ['51job.com']
    start_urls = ['http://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    def parse(self, response):
        items = []
        # 选取每一个页面的职位信息
        for each in response.xpath('//div[@class="dw_table"]/div[@class="el"]'):
            #创建对象
            item = FiveOneJobItem()
            # 提取出相应的字段
            jobtitle = each.xpath('p/span/a/text()').extract()
            link = each.xpath('p/span/a/@href').extract()
            company = each.xpath('span[@class="t2"]/a/@title').extract()
            location = each.xpath('span[@class="t3"]/text()').extract()
            money = each.xpath('span[@class="t4"]/text()').extract()
            if len(money) == 0:
                money = ["null"]
            update_time = each.xpath('span[@class="t5"]/text()').extract()

            item['jobtitle'] = jobtitle[0].strip()
            item['link'] = link[0]
            item['company'] = company[0]
            item['location'] = location[0]
            item['money'] = money[0]
            item['update_time'] = update_time[0]

            #提取职位详情和公司详情
            yield scrapy.Request(item['link'],meta={'position':item},callback=self.parse_position)

        #获取当前页码
        now_pagenumber = response.xpath('//div[@class="dw_page"]/div[@class="p_box"]/div[@class="p_wp"]/div[@class="p_in"]/ul/li[@class="on"]/text()').extract()[0]
        url = "http://search.51job.com/list/010000,000000,0000,00,9,99,python,2,"+str(int(now_pagenumber)+1)+".html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        #判断是否到达尾页
        if response.xpath("//li[@class='bk'][last()]/a/@href"):
            #发送下一页请求
            yield scrapy.Request(url=url,callback=self.parse)

    #获取职位详情和公司详情函数
    def parse_position(self,response):
        item = response.meta['position']

        zhize_list = response.xpath("//div[@class='bmsg job_msg inbox']/text()").extract()
        zhize = "".join(zhize_list)
        zhize_rnt = re.compile(r'[\r\n\t]')
        result_rnt = zhize_rnt.sub("",zhize)
        item['position_zhize'] = result_rnt.strip()

        company_list = response.xpath("//div[@class='tmsg inbox']/text()").extract()
        company = "".join(company_list)
        company_rnt = re.compile(r'[\r\n\t]')
        company_rnt = company_rnt.sub("",company)
        item['position_company'] = result_rnt.strip()

        #提交给管道
        yield item
