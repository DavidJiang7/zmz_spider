from spider.zmz_link_base_spider import zmz_link_base_spider

# 爬取下载链接
s = zmz_link_base_spider()
s.init_resource_base()
print('增量爬取下载链接结束......')