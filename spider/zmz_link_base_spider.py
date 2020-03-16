import requests, logging, time, pdb, random, traceback
from datetime import datetime
from storage.manager import ZMZManager
from utils.http import UrlTool, Http
from lxml import etree
from model.items import Resource, ResourceBase
from utils.web import WebSelenium

# 获取 资源的唯一 code，并初始化爬取链接的数据
class zmz_link_base_spider():
    def __init__(self):
        self.pc_url = 'http://got001.com/resource.html?code={code}'
        self.m_api_url = 'http://m.got001.com/api/v1/static/resource/detail?code={code}'
        self.Http = Http()
        self.ZMZManager = ZMZManager()
        self.WebSelenium = WebSelenium()

    def init_resource_base(self):
        pageSize = 20
        while True:
            resources = self.ZMZManager.get_resource(pageSize)
            if (resources is None or len(resources) == 0):
                break
            else:
                for res in resources:
                    # html = self.Http.get_html(res['Url'])
                    html = self.WebSelenium.get_html(res['Url'])
                    if html is None or html == '':
                        print(resourceId, '被屏蔽，后续可重试...')
                        self.ZMZManager.update_resource_status(res['Id'], 2)   # 被屏蔽，可重试
                        continue
                    self.get_resource_base(html, res['Id'])
                    secends = random.randint(1, 10)
                    time.sleep(secends)
            if len(resources) < pageSize:
                break
        
    # 查找资源链接code，初始化链接采集基础信息
    def get_resource_base(self, html, resourceId):
        tree = etree.HTML(html)
        box = tree.xpath('//div[@id="resource-box"]')
        # pdb.set_trace()
        if box is None or len(box) == 0:
            print(resourceId, '找不到链接code...')
            self.ZMZManager.update_resource_status(resourceId, 3)   # 找不到链接code，可重试
            return
        # 由于版权原因资源关闭
        if etree.tostring(box[0], encoding='utf8').decode('utf8').find('版权') > -1:
            print(resourceId, '资源被屏蔽...')
            self.ZMZManager.update_resource_status(resourceId, 4)   # 版权被封，短时间内不会开放
            return
        a = box[0].xpath('./div//a[@href]')[0]
        # pdb.set_trace()
        if a is not None:
            href = a.get('href', '')
            if href != '':
                code = str(UrlTool.url_query_param(href,'code',default_value='',encoding='utf-8'))
                if code != '':
                    rb = ResourceBase()
                    rb['Id'] = resourceId
                    rb['Code'] = code
                    rb['PCApi'] = self.pc_url.format(code=code)
                    rb['MApi'] = self.m_api_url.format(code=code)
                    print(rb)
                    self.ZMZManager.insert_data(rb, 'ResourceBase')                    
                    self.ZMZManager.update_resource_status(res['Id'], 1)   # 成功
                else:
                    # 未知情况
                    self.ZMZManager.update_resource_status(res['Id'], 5)   # 未知情况