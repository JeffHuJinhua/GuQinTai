# -*- coding: utf-8 -*-
import scrapy
from performance.spiders.parse_table import table_parse

class WhxcSpider(scrapy.Spider):
    name = 'whxc'
    allowed_domains = ['www.whxc.org.cn']

    start_urls = ['http://www.whxc.org.cn/zt/xcbwhwc/yszc/ycjz']

    def art_content_parse(self, response):
        # 打印出表格标题作为提示
        # print(response.xpath('/html/body/section/div[2]/article/div[2]/div/p[1]/text()').extract_first())
        table_parse(response, '/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody')
        # print(response.xpath('/html/body/section/div[2]/article/div[2]/div/p[5]/text()').extract_first())
        table_parse(response, '/html/body/section/div[2]/article/div[2]/div/div[2]/table/tbody')
        # print(response.xpath('/html/body/section/div[2]/article/div[2]/div/p[15]/text()').extract_first())
        table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table[1]/tbody')
        # print(response.xpath('/html/body/section/div[2]/article/div[2]/div/p[17]/text()').extract_first())
        table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table[2]/tbody')
        # print(response.xpath('/html/body/section/div[2]/article/div[2]/div/p[20]/text()').extract_first())
        table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table[3]/tbody')

    def paint_content_parse(self, response):
        # 打印出表格标题作为提示
        print(response.xpath('/html/body/section/div[2]/article/h1/text()').extract_first())
        table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table/tbody')

    def parse(self, response):
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
        # 对二维列表[href, title] 遍厉，根据 title 选择内容页面做相应的数据爬取
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
