# -*- coding: utf-8 -*-
import scrapy
import string


class WhxcSpider(scrapy.Spider):
    name = 'whxc'
    allowed_domains = ['www.whxc.org.cn']

    start_urls = ['http://www.whxc.org.cn/zt/xcbwhwc/yszc/ycjz']
    # print('in the whxc2.py spider...')

    def xpath_name(self, response, show_name, i_row, i_col, show_xpath):
        # 初始化 span 方向的标志 row_col ：0-行合并；1-列合并
        row_col = 0

        # 读取指定单元 row, col 中的全部文本： //text()
        show_names = response.xpath(show_xpath + '//text()', tr_pos=i_row+1, td_pos=i_col).extract()

        # 初始化变量 show_cell 用于拆解读取的单元内容 show_names[] 列表成字符串，填充 show_name
        show_cell = ''
        if show_names != []:
            if len(show_names) > 1:
                for i_names in range(0, len(show_names)):
                    show_cell += show_names[i_names]
            else:
                show_cell = show_names[0]
            show_name.append(show_cell)

        # 判断是否有单元格的行合并或列合并，按合并数-1继续填充 show_name，最后在首位补行合并标志 0，列合并标志 1
        i_rowspan = response.xpath(show_xpath + '/@rowspan', tr_pos=i_row + 1, td_pos=i_col).extract_first()
        if  i_rowspan is not None:
            for i in range(int(i_rowspan)-1):
                show_name.append(show_cell)
            row_col = 0
        i_colspan = response.xpath(show_xpath + '/@colspan', tr_pos=i_row + 1, td_pos=i_col).extract_first()
        if i_colspan is not None:
            for i in range(int(i_colspan)-1):
                show_name.append(show_cell)
            row_col = 1

        show_name.insert(0, row_col)

        return show_name

    def table_parse(self, response, table_xpath):
        # 直接读取表格总行数 row
        row = len(response.xpath(table_xpath + '/tr').extract())
        # 通过第二行开始的内容行读取表格的总列数：col，默认表格的第一条内容行没有行或列的合并
        col = len(response.xpath(table_xpath+'/tr[position()=2]/td').extract())
        # 根据表格的总行列数，初始化空的表格二维列表和相对应的标志二维列表
        show_table = [[0 for col in range(col)] for row in range(row)]
        table_flag = [[0 for col in range(col)] for row in range(row)]
        for r in range(row):
            td_pos_off = 1
            c = 0
            while c < col:
                show_name = []
                show_xpath = table_xpath + '/tr[position()=$tr_pos]/td[position()=$td_pos]'
                if table_flag[r][c] == 1:
                    td_pos_off -= 1
                    c += 1
                    continue
                show_name = self.xpath_name(response, show_name, r, c+td_pos_off, show_xpath)
                for n in range(len(show_name)-1):
                    if show_name[0] == 0:
                        show_table[r+n][c] = show_name[n+1]
                        table_flag[r+n][c] = 1
                    elif show_name[0] == 1:
                        show_table[r][c+n] = show_name[n+1]
                        table_flag[r][c+n] = 1
                c += 1
        # 打印出已爬取的表格的二维列表
        for r2 in range(row):
            print(show_table[r2])

    def art_content_parse(self, response):
        # 打印出表格标题作为提示
        # print(response.xpath('/html/body/section/div[2]/article/h1/text()').extract_first())
        self.table_parse(response, '/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody')
        self.table_parse(response, '/html/body/section/div[2]/article/div[2]/div/div[2]/table/tbody')
        self.table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table[1]/tbody')
        self.table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table[2]/tbody')
        self.table_parse(response, '/html/body/section/div[2]/article/div[2]/div/table[3]/tbody')

    def paint_content_parse(self, response):
        # 打印出表格标题作为提示
        print(response.xpath('/html/body/section/div[2]/article/h1/text()').extract_first())
        # 直接读取表格总行数 row
        row = len(response.xpath('/html/body/section/div[2]/article/div[2]/div/table/tbody/tr').extract())
        # 通过第二行开始的内容行读取表格的总列数：col，默认表格的第一条内容行没有行或列的合并
        col = len(response.xpath('/html/body/section/div[2]/article/div[2]/div/table/tbody/tr[position()=2]/td').extract())
        # 根据表格的总行列数，初始化空的表格二维列表和相对应的标志二维列表
        show_table = [[0 for col in range(col)] for row in range(row)]
        table_flag = [[0 for col in range(col)] for row in range(row)]
        for r in range(row):
            td_pos_off = 1
            c = 0
            while c < col:
            #for c in range(col):
                show_name = []
                show_xpath = '/html/body/section/div[2]/article/div[2]/div/table/tbody/tr[position()=$tr_pos]/td[position()=$td_pos]'
                if table_flag[r][c] == 1:
                    td_pos_off -= 1
                    c += 1
                    continue
                show_name = self.xpath_name(response, show_name, r, c+td_pos_off, show_xpath)
                for n in range(len(show_name)-1):
                    if show_name[0] == 0:
                        show_table[r+n][c] = show_name[n+1]
                        table_flag[r+n][c] = 1
                    elif show_name[0] == 1:
                        show_table[r][c+n] = show_name[n+1]
                        table_flag[r][c+n] = 1
                c += 1
        # 打印出已爬取的表格的二维列表
        for r2 in range(row):
            print(show_table[r2])

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

