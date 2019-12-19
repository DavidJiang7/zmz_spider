import pdb, json, random, time, traceback
from datetime import datetime
from utils.http import Http
from bs4 import BeautifulSoup
from model.items import SearchResult
from storage.manager import ZMZManager


class Search():
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
                    k.append(res['NameCN'])
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
                url = self.url.format(keyword='+'.join(keyword_array), page=page)
                html = self.Http.get_html(url)
                bs = BeautifulSoup(html, features='lxml')
                link_list = bs.find_all('ul', class_='link-list')
                if link_list and len(link_list) > 0:
                    for link in link_list:
                        li = link.find('li')
                        span = link.find('span', class_='name')
                        sr = SearchResult()
                        sr['ResourceId'] = resouceId
                        sr['LinkId'] = int(li.get('data-id', '0'))
                        sr['Title'] = span.text.strip()
                        sr['MagnetUrl'] = li.get('data-magnet', '')
                        sr['Ed2kUrl'] = li.get('data-ed2k', '')
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
            self.ZMZManager.update_resource_link(item)

        

