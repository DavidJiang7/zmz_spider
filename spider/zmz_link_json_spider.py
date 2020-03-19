import requests, logging, time, pdb, random, traceback
from datetime import datetime
from storage.manager import ZMZManager
from utils.http import UrlTool, Http
from model.items import Resource, ResourceBase
from utils.web import WebSelenium

class zmz_link_json_spider():
    def __init__(self):
        self.Http = Http()
        self.ZMZManager = ZMZManager()
        
    def get_resource_json(self):
        pageSize = 20
        while True:
            resources = self.ZMZManager.get_resource_base(pageSize)
            if (resources is None or len(resources) == 0):
                break
            else:
                for res in resources:
                    # html = self.Http.get_html(res['Url'])
                    html = self.Http.get_html(res['MApi'])
                    if html is None or html == '':
                        print(resourceId, '被屏蔽，后续可重试...')
                        # 0-未更新json，1-完成解析，2-正在解析json，3-解析json异常，4-被屏蔽拿不到json
                        self.ZMZManager.update_resource_base_status(res['Id'], 4)   # 被屏蔽，可重试
                        continue
                    self.ZMZManager.update_resource_base_json(res['Id'], html)
                    secends = random.randint(1, 10)
                    time.sleep(secends)
            if len(resources) < pageSize:
                break 