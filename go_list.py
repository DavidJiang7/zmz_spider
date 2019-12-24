from spider.zmz_list_spider import zmz_list_spider

# 增量爬取资源
s = zmz_list_spider()
s.go()
print('增量爬取资源结束......')