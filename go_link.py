from spider.zmz_link_search_spider import zmz_link_search_spider

# 爬取下载链接
s = zmz_link_search_spider()
s.go()
print('增量爬取下载链接结束......')