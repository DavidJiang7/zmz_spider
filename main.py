from spider.zmz_list_spider import zmz_list_spider
from spider.zmz_link_search_spider import zmz_link_search_spider
from utils.http import UrlTool

# 增量爬取资源
s = zmz_list_spider()
s.go()
input()

# # 爬取下载链接
# s = Search()
# s.go()
# print('爬取下载链接结束......')

# s = '【美剧】《越狱权力的游戏》'
# ss = s[s.index('《')+1:s.index('》')]
# print(ss)