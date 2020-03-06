import requests, logging, time, pdb, random, traceback
from datetime import datetime
from storage.manager import ZMZManager
from utils.http import UrlTool, Http
from lxml import etree
from model.items import Resource, ResourceBase
from utils.web import WebSelenium


class zmz_link_spider():
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
                        continue
                    self.get_resource_base(html, res['Id'])
                    self.ZMZManager.update_resource_status(res['Id'])   
                    time.sleep(random.randint(1, 1))
            if len(resources) < pageSize:
                break
        
    # 查找资源链接code，初始化链接采集基础信息
    def get_resource_base(self, html, resourceId):
        tree = etree.HTML(html)
        box = tree.xpath('//div[@id="resource-box"]')[0]
        a = box.xpath('./div//a[@href]')[0]
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
                    print('code：', rb)
                    self.ZMZManager.insert_data(rb, 'ResourceBase')
