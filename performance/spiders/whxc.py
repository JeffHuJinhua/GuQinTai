# -*- coding: utf-8 -*-
import scrapy
from performance.spiders.parse_table import table_parse
from scrapy.loader import ItemLoader
from performance.items import PerformanceItem
import pymongo
from scrapy.conf import settings


class WhxcSpider(scrapy.Spider):
    name = 'whxc'
    allowed_domains = ['www.whxc.org.cn']

    start_urls = ['http://www.whxc.org.cn/zt/xcbwhwc/yszc/ycjz']

    def art_content_parse(self, response):
        # Using Item Loaders to populate items
        item_loader = ItemLoader(item=PerformanceItem(), response=response)

        # 打印出表格标题作为提示
        # print(response.xpath('/html/body/section/div[2]/article/div[2]/div/p[1]/text()').extract_first())
        show_table = table_parse(response, '/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody')
        # print(response.xpath('/html/body/section/div[2]/article/div[2]/div/p[5]/text()').extract_first())
        # 打印出已爬取的表格的二维列表
        for r in range(len(show_table)):
            # print(show_table[r])
            # print(type(show_table[r][1]))
            item_loader.add_value('name', show_table[r][0])
            item_loader.add_value('date', show_table[r][1])
            item_loader.add_value('place', show_table[r][2])

        show_table = table_parse(response, '/html/body/section/div[2]/article/div[2]/div/div[2]/table/tbody')
        for r in range(len(show_table)):
            item_loader.add_value('name', show_table[r][0])
            item_loader.add_value('date', show_table[r][1])
            item_loader.add_value('place', show_table[r][2])

        show_table = table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table[1]/tbody')
        # print(response.xpath('/html/body/section/div[2]/article/div[2]/div/p[17]/text()').extract_first())
        for r in range(len(show_table)):
            item_loader.add_value('name', show_table[r][0])
            item_loader.add_value('date', show_table[r][1])
            item_loader.add_value('place', show_table[r][2])

        show_table = table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table[2]/tbody')
        # print(response.xpath('/html/body/section/div[2]/article/div[2]/div/p[20]/text()').extract_first())
        for r in range(len(show_table)):
            item_loader.add_value('name', show_table[r][0])
            item_loader.add_value('date', show_table[r][1])
            item_loader.add_value('place', show_table[r][2])

        show_table = table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table[3]/tbody')
        for r in range(len(show_table)):
            item_loader.add_value('name', show_table[r][0])
            item_loader.add_value('date', show_table[r][1])
            item_loader.add_value('place', show_table[r][2])

        print(item_loader.load_item())
        return item_loader.load_item()

    def paint_content_parse(self, response):
        # Using Item Loaders to populate items
        item_loader = ItemLoader(item=PerformanceItem(), response=response)

        # 打印出表格标题作为提示
        print(response.xpath('/html/body/section/div[2]/article/h1/text()').extract_first())
        show_table = table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table/tbody')
        for r in range(len(show_table)):
            item_loader.add_value('name', show_table[r][1])
            item_loader.add_value('date', show_table[r][2])
            item_loader.add_value('place', show_table[r][2])

        return item_loader.load_item()

    def parse(self, response):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        sheetname = settings['MONGODB_SHEETNAME']
        # 创建 MONGODB 数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        db = client[dbname]
        # 存放数据的数据库表名
        self.post = db[sheetname]

        # 从爬虫开始的目录首页里，获得内容页面的标题名称和链接的列表
        page_list = response.xpath('/html/body/section/div[3]/article/dl/dd/h2/a/@href').extract()
        title_list = response.xpath('/html/body/section/div[3]/article/dl/dd/h2/a/text()').extract()
        # 合并成一个二维列表[href, title]
        page_title_list = []
        for i in range(0,len(page_list)):
            if i == 0:
                page_title_list = [[page_list[0], title_list[0]]]
            else:
                page_title_list.append([page_list[i], title_list[i]])
        # 对二维列表[href, title] 遍历，根据 title 选择内容页面做相应的数据爬取
        for page in page_title_list:
            print(page[0])
            print(page[1])
            if page[1].startswith('武汉市文艺活动信息'):
                print('in the 武汉市文艺活动信息')
                yield scrapy.Request(page[0], callback=self.art_content_parse)
            elif page[1].startswith('武汉美术馆展览活动'):
                print('in the 武汉美术馆展览' + page[0])
                yield scrapy.Request(page[0], callback=self.paint_content_parse)

        # 回调，爬取下一页，直至最后一页 'next disable' 结束
        if response.xpath('/html/body/section/div[3]/article/div/ul/li[9]/a/@class') != 'next disable':
            url = (response.xpath('/html/body/section/div[3]/article/div/ul/li[9]/a/@href').extract_first())
            yield scrapy.Request(url=url, callback=self.parse)
