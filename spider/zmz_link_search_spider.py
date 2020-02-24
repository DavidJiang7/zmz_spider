import pdb, json, random, time, traceback
from datetime import datetime
from utils.http import Http
from lxml import etree
from model.items import ResourceLink
from storage.manager import ZMZManager
from urllib import parse


class zmz_link_search_spider():
    def __init__(self):
        self.url = 'http://oabt007.com/index/index/k/{keyword}/p/{page}'
        self.Http = Http()
        self.ZMZManager = ZMZManager()
    
    def go(self):
        pageSize = 20
        while True:
            resources = self.ZMZManager.get_resource(pageSize)
            if (resources is None or len(resources) == 0):
                break
            else:
                for res in resources:
                    k = []
                    namecn = res['NameCN'].replace('/', ' ')
                    nameen = res['NameEN'].replace('/', ' ')
                    if not namecn or not nameen:
                        continue
                    k.append(namecn)
                    k.append(nameen)
                    self.get(res['Id'], k)
                    time.sleep(random.randint(5, 10))
            if len(resources) < pageSize:
                break

    def get(self, resouceId, keyword_array):
        result = []
        page = 1
        while True:
            try:
                #pdb.set_trace()
                url = self.url.format(keyword=parse.quote(' '.join(keyword_array),encoding='utf-8'), page=page)
                print("当前搜索url：" + url)
                html = self.Http.get_html(url)
                tree = etree.HTML(html)
                link_list = tree.xpath('//div[@class="link-list-wrapper"]/ul[@class="link-list"]/li[@data-id]')
                if link_list and len(link_list) > 0:
                    for link in link_list:
                        # pdb.set_trace()
                        span = link.xpath('./span[@class="name"]')
                        sr = ResourceLink()
                        sr['ResourceId'] = resouceId
                        sr['LinkId'] = int(link.get('data-id', '0'))
                        sr['Title'] = span[0].text.strip()
                        sr['MagnetUrl'] = link.get('data-magnet', '')
                        sr['Ed2kUrl'] = link.get('data-ed2k', '')
                        if sr['MagnetUrl'].find("magnet:") == -1:
                            sr['MagnetUrl'] = ''
                        if sr['Ed2kUrl'].find("ed2k:") == -1:
                            sr['Ed2kUrl'] = ''
                        if sr['MagnetUrl'] == '' and sr['Ed2kUrl'] == '':
                            continue
                        print(sr)
                        result.append(sr)
                        self.insert(sr)
                else:
                    break
                page += 1
                time.sleep(random.randint(1, 5))
            except:
                traceback.print_exc() # 打印错误代码行
                time.sleep(random.randint(300, 600))     
        self.ZMZManager.update_resource_status(resouceId)   
        return result

    def insert(self, item):
        info = self.ZMZManager.get_one_resource_link(item['ResourceId'], item['LinkId'])
        if info is None:
            self.ZMZManager.insert_resource_link(item)
        else:
            item['Id'] = info['Id']
            self.ZMZManager.update_resource_link(item)

        

