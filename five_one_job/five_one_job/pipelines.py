# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class FiveOneJobPipeline(object):
    def __init__(self):
        self.file = open('job.json','w')

    def process_item(self, item, spider):
        # json数据中添加逗号和换行符
        content = json.dumps(dict(item),ensure_ascii = False) + ",\n"
        self.file.write(content)
        return item

    def close_spider(self,spider):
        self.file.close()
