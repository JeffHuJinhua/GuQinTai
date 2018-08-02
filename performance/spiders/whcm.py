# -*- coding: utf-8 -*-
import scrapy
from performance.spiders.parse_table import table_parse
from scrapy.loader import ItemLoader
from performance.items import PerformanceItem
import pymongo
from scrapy.conf import settings


class WhcmSpider(scrapy.Spider):
    name = 'whcm'
    allowed_domains = ['yssj.whcm.edu.cn']
    start_urls = ['http://yssj.whcm.edu.cn/ycxx.htm']
    is_first_page = True

    def content_parse(self, response):
        # Using Item Loaders to populate items
        item_loader = ItemLoader(item=PerformanceItem(), response=response)

        # 打印出表格标题作为提示
        print(response.xpath('//*[@id="page42299"]/div/h2/text()').extract_first())
        show_table = table_parse(response, '//*[@id="vsb_content_2"]/div/table/tbody')
        # 打印出已爬取的表格的二维列表
        for r in range(len(show_table)):
            print(show_table[r])
            print(type(show_table[r][1]))
            item_loader.add_value('name', show_table[r][1])
            item_loader.add_value('date', show_table[r][0])
            item_loader.add_value('place', show_table[r][2])
            # print(item_loader.load_item())
            # return item_loader.load_item
        print(item_loader.load_item())
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
        page_list = response.xpath('//td[2]/a/@href').extract()
        title_list = response.xpath('//td[2]/a/text()').extract()
        # 合并成一个二维列表[href, title]
        page_title_list = []
        for i in range(0,len(page_list)):
            if i == 0:
                page_title_list = [[page_list[0], title_list[0]]]
            else:
                page_title_list.append([page_list[i], title_list[i]])
        # 对二维列表[href, title] 遍历，先用 start_urls[0] 截取主域名用来补齐 href
        for page in page_title_list:
            print(page[1], end=':')
            full_url = self.start_urls[0][:-8] + page[0]
            print(full_url)
            print('in the 武汉音乐学院')
            # 如果在 mongodb 中没有找到要爬取的页面，将 url 写入 mongodb 中，并回调爬取页面
            if self.post.find_one({'url': full_url}) is None:
                self.post.insert({'url': full_url})
                yield scrapy.Request(full_url, callback=self.content_parse)
            # 如果在 mongodb 中找到要爬取的页面，将 pass 不再重复爬取
            pass

        # 回调，爬取下一页，直至最后一页 'NextDisabled' 结束
        if response.xpath('//*[@id="CicroQ4UCG3_2848_0473_ky_25__content"]/div/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/span[1]/@class') != 'NextDisabled':
            if self.is_first_page:
                url = response.xpath('//*[@id="CicroQ4UCG3_2848_0473_ky_25__content"]/div/div//@href').extract()[0]
                self.is_first_page = False
            else:
                url = response.xpath('//*[@id="CicroQ4UCG3_2848_0473_ky_25__content"]/div/div//@href').extract()[2]
            full_url = self.start_urls[0][:-8] + url
            yield scrapy.Request(url=full_url, callback=self.parse)
