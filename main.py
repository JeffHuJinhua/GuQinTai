#import h_scrapy
#import h_save
#import h_show
from scrapy import cmdline

# scrapy.cmdline.execute 方法只限于，快速调试的作用或一个项目下单个 spider 的爬行任务！
# cmdline.execute('scrapy crawl whxc --nolog'.split())

cmdline.execute('scrapy crawlall --nolog'.split())
