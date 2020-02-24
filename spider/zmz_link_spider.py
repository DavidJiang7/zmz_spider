import requests, logging, time, pdb, random, traceback
from datetime import datetime
from storage.manager import ZMZManager
from utils.http import UrlTool, Http
from lxml import etree
from model.items import Resource, ResourceBase


class zmz_link_spider():
    def __init__(self):
        # self.pc_url = 'http://got001.com/resource.html?code={code}'
        self.m_api_url = 'http://m.got001.com/api/v1/static/resource/detail?code={code}'
        self.Http = Http()
        self.ZMZManager = ZMZManager()

    def init_resource_base(self):
        pageSize = 20
        while True:
            resources = self.ZMZManager.get_resource(pageSize)
            if (resources is None or len(resources) == 0):
                break
            else:
                for res in resources:
                    html = self.Http.get_html(res['Url'])
                    self.get_resource_base(html, res['Id'])
                    time.sleep(random.randint(1, 3))
            if len(resources) < pageSize:
                break
    
    # 获取网页上的资源链接地址
    def get_resource_base(self, html, resourceId):
        tree = etree.HTML(html)
        a = tree.xpath('//div[@id="resource-box"]/div[@class="view-res-list"]/div[contains(@class,"view-res-tips")]/a[@href]')
        if a:
            href = a.get('href', '')
            if href != '':
                code = str(UrlTool.url_query_param(href,'code',default_value='',encoding='utf-8'))
                if code != '':
                    self.get_resource_from_api(code, resourceId)
        pass

    def get_resource_from_api(self, code, resourceId):
        
        rb = ResourceBase()
        rb['Id'] = resourceId
        rb['Code'] = code
        rb['Code'] = code
        rb['Code'] = code
        rb['Code'] = code
        rb['Code'] = code
        rb['Code'] = code
        rb['Code'] = code
        rb['Code'] = code
        rb['Code'] = code
        rb['Code'] = code
        rb['Code'] = code
