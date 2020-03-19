from spider.zmz_link_json_spider import zmz_link_json_spider

# 爬取下载链接
s = zmz_link_json_spider()
s.get_resource_json()
print('结束......')