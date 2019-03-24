# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class LianjiaPipeline(object):
    conn = None
    cursor = None

    def open_spider(self, spider):
        print('爬虫开始')
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='', db='lianjia', charset='utf8')

    def process_item(self, item, spider):
        sql = "insert into zufang values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
              (item['district'], item['street'], item['plot'], item['time'], item['money'],
               item['typ'], item['area'], item['orientation'], item['subway'], item['longitude'],
               item['latitude'])
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        print('爬虫结束')
        self.cursor.close()
        self.conn.close()
