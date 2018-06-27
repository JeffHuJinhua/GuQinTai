# -*- coding: utf-8 -*-
import scrapy
import string

class WhxcSpider(scrapy.Spider):
    name = 'whxc'
    allowed_domains = ['www.whxc.org.cn']
    start_urls = ['http://www.whxc.org.cn/zt/xcbwhwc/yszc/ycjz/1.shtml']

    def content_parse(self, response):

        show_name = []
        show_date = []
        show_place = []
        show_price = []
        show_contact = []
        show_productor = []
        for i_row in range(1, 30):
            print('===>' + str(i_row))

            if len(show_name) < i_row:
                show_temp = ''
                show_names = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="170"]/p/text()', i_pos=i_row+1).extract()
                if show_names != []:
                    if len(show_names) > 1:
                        for i_names in range(0,len(show_names)):
                            show_temp += show_names[i_names]
                    else:
                        show_temp = show_names[0]
                    show_name.append(show_temp)
                    for i_rowspan in range(2, 9):
                        if response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="170"]/@rowspan', i_pos=i_row+1).extract_first() == str(i_rowspan):
                            for show_name_appends in range(1, i_rowspan):
                                show_name.append(show_temp)

            if len(show_date) < i_row:
                show_temp = ''
                show_dates = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="121"]/p/text()', i_pos=i_row+1).extract()
                if show_dates != []:
                    if len(show_dates) > 1:
                        for i_dates in range(0, len(show_dates)):
                            show_temp += show_dates[i_dates]
                    else:
                        show_temp = show_dates[0]
                    show_date.append(show_temp)
                    for i_rowspan in range(2, 9):
                        if response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="121"]/@rowspan', i_pos=i_row + 1).extract_first() == str(i_rowspan):
                            for show_date_appends in range(1, i_rowspan):
                                show_date.append(show_temp)

            if len(show_place) < i_row:
                show_temp = ''
                show_temp2 = ''
                show_places = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="95"]/p/text()', i_pos=i_row+1).extract()
                #print(show_places)
                if show_places != []:
                    if len(show_places) > 1:
                        for i_names in range(0,len(show_places)):
                            show_temp += show_places[i_names]
                    else:
                        show_temp = show_places[0]
                    if show_temp[-8:].isdigit():
                        show_temp2 = show_temp[-8:]
                    show_temp = show_temp.rstrip(string.digits)
                    print(show_temp + ' temp | temp2 ' + show_temp2)
                    show_place.append(show_temp)
                    if show_temp2 != '':
                        show_contact.append(show_temp2)
                    rowspans = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="95"]/@rowspan', i_pos=i_row + 1).extract()
                    if rowspans != []:
                        if len(rowspans) == 1:
                            if not response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="95" and @rowspan=$i_row]/p/text()',i_pos=i_row + 1,i_row=rowspans[0]).extract_first().isdigit():
                                for i_rowspan in range(2, 9):
                                    if rowspans[0] == str(i_rowspan):
                                        for show_place_appends in range(1, i_rowspan):
                                            show_place.append(show_temp)
                            else:
                                print('in the contact===')
                                if show_temp2.isdigit():
                                    for i_rowspan in range(2, 9):
                                        if rowspans[0] == str(i_rowspan):
                                            for show_place_appends in range(1, i_rowspan):
                                                show_contact.append(show_temp2)
                        if len(rowspans) == 2:
                            for i_rowspan in range(2, 9):
                                if rowspans[0] == str(i_rowspan):
                                    for show_place_appends in range(1, i_rowspan):
                                        show_place.append(show_temp)
                            for i_rowspan in range(2, 9):
                                if rowspans[1] == str(i_rowspan):
                                    for show_place_appends in range(1, i_rowspan):
                                        show_contact.append(show_temp2)

            if len(show_price) < i_row:
                show_temp = ''
                show_names = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="114"]/p/text()', i_pos=i_row+1).extract()
                if show_names != []:
                    if len(show_names) > 1:
                        for i_names in range(0,len(show_names)):
                            show_temp += show_names[i_names]
                    else:
                        show_temp = show_names[0]
                    show_price.append(show_temp)
                    for i_rowspan in range(2, 9):
                        if response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="114"]/@rowspan', i_pos=i_row+1).extract_first() == str(i_rowspan):
                            for show_name_appends in range(1, i_rowspan):
                                show_price.append(show_temp)

            if len(show_productor) < i_row:
                show_temp = ''
                show_names = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="99"]/p/text()', i_pos=i_row+1).extract()
                if show_names != []:
                    if len(show_names) > 1:
                        for i_names in range(0,len(show_names)):
                            show_temp += show_names[i_names]
                    else:
                        show_temp = show_names[0]
                    show_productor.append(show_temp)
                    for i_rowspan in range(2, 9):
                        if response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$i_pos]/td[@width="99"]/@rowspan', i_pos=i_row+1).extract_first() == str(i_rowspan):
                            for show_name_appends in range(1, i_rowspan):
                                show_productor.append(show_temp)

            #print(i_row)
            print(len(show_name))
            print(show_name)
            print(len(show_date))
            print(show_date)
            print(len(show_place))
            print(show_place)
            print(len(show_price))
            print(show_price)
            print(len(show_contact))
            print(show_contact)
            print(len(show_productor))
            print(show_productor)

            #date = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()=$ii]/td[2]/p[1]/text()', ii=i_row+1).extract()
            #if date is None:
            #    show_date += show_date[i-1]
            #else:
            #show_date += date


        #name2 = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[3]/td[1]/p/text()').extract()
        #date = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()<=last()]/td[2]/p[1]/text()').extract()
        #time = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()<=last()]/td[2]/p[2]/text()').extract()
        #place = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()<=last()]/td[3]/p/text()').extract()
        #price = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()<=last()]/td[4]/p/text()').extract()
        #contact = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()<=last()]/td[5]/p/text()').extract()
        #productor = response.xpath('/html/body/section/div[2]/article/div[2]/div/div[1]/table/tbody/tr[position()<=last()]/td[6]/p/text()').extract()

        #print(name)
        #print(date)
        #print(time)
        #print(place)
        #print(price)
        #print(contact)
        #print(productor)

    def parse(self, response):
        #pass
        page_list = response.xpath('/html/body/section/div[3]/article/dl/dd/h2/a/@href').extract()
        print(page_list)
        for page in page_list:
            yield scrapy.Request(page, callback=self.content_parse)