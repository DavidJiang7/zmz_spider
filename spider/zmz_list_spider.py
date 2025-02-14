import requests, logging, time, pdb, random, traceback
from datetime import datetime
from bs4 import BeautifulSoup
from storage.manager import ZMZManager
from utils.http import UrlTool, Http
from lxml import etree
from model.items import Resource, ResourceProp, Character, ResourceCharacter
from spider.zmz_link_spider import zmz_link_spider

# 字幕组->资源库->资源列表爬取
class zmz_list_spider():
    domain = 'http://www.rrys2019.com'

    def __init__(self, name=None, **kwargs):
        self.ZMZManager = ZMZManager()
        self.Http = Http()
        self.ZMZLinkSpider = zmz_link_spider()

    def go(self):
        channel_list = self.ZMZManager.get_channel_list()
        if channel_list is None or len(channel_list) == 0:
            return
        for it in channel_list:
            # print(it)
            #time.sleep(10) #停顿10秒
            html = self.Http.get_html(it['Url'])
            self.spider_list(html, it['Channel'])
            self.ZMZManager.update_channel_list(it['Id'])
            time.sleep(30)

    def spider_list(self, html, channel):
        tree = etree.HTML(html)
        lis = tree.xpath('//div[contains(@class,"resource-showlist")]/ul/li[@class="clearfix"]')
        if lis and len(lis) > 0:
            for li in lis:
                # pdb.set_trace()
                a = li.xpath('./div[@class="fl-img"]/a[@href]')[0]
                span = a.xpath('./span[contains(@class,"point")]')[0]
                score = ''.join(span.xpath('.//text()')).replace('"', '')
                href = a.get('href', '')
                id = int(href.rsplit('/', 1)[1])
                # if self.ZMZManager.is_exist_resource(id) == True:
                #     continue
                # else:
                #     self.spider_resource(a['href'], span.text.replace('"', ''), channel_list_obj['Channel']) 
                self.spider_resource(href, score, channel)       
                time.sleep(3)        

    # 获取资源基础信息
    def spider_resource(self, url, score, channel):
        # pdb.set_trace()
        print(url, score)
        url = self.domain + url
        html = self.Http.get_html(url)
        bs = BeautifulSoup(html, features='lxml')
        div_tit = bs.find('div', class_='resource-tit')
        div_con = bs.find('div', class_='resource-con')
        div_desc = bs.find('div', class_='resource-desc')
        ul_li = []
        try:
            ul_li = div_con.find('div', class_='fl-info').find('ul').find_all('li')
        except:
            pass
        res = Resource()
        try:
            res['Id'] = int(url.rsplit("/",1)[1])
            res['Url'] = url
            res['Score'] = float(score)
            res['OtherName'] = ''
            try:
                name = div_tit.find('h2').text.replace('[RSS]', '').lstrip('"').rstrip('"').strip()
                res['NameCN'] = name[name.index('《')+1:name.index('》')]
            except:
                res['NameCN'] = ''
            try:
                res['NameEN'] = ul_li[0].find('strong').text.strip()
            except:
                res['NameEN'] = ''
            try:
                res['PlayStatus'] = div_tit.find('label', id='play_status').text.strip()
            except:
                res['PlayStatus'] = ''
            try:
                res['Explain'] = div_tit.find('p').text
            except:
                res['Explain'] = ''
            try:
                res['ImgLink'] = div_con.find('div', class_='imglink').find('a')['href']
            except:
                res['ImgLink'] = ''
            try:
                # eg: http://js.jstucdn.com/images/level-icon/e-big-1.png
                level = div_con.find('div', class_='level-item').find('img')['src']      
                res['Level'] = level.rsplit("/",1)[1][0]
            except:
                res['Level'] = ''
            try:
                res['Description'] = div_desc.find_all('div')[-1].text
            except:
                res['Description'] = ''
            # pdb.set_trace()
            res['CreateTime'] = datetime.now()
            res['UpdateTime'] = datetime.now()
            res['Channel'] = channel
            try:
                rss = div_tit.find('h2').find('a')
                if rss is None:
                    res['RSSUrl'] = ''
                else:
                    res['RSSUrl'] = rss['href']
            except:
                res['RSSUrl'] = ''
                pass
            print('资源',res)
            if self.ZMZManager.is_exist_resource(res['Id']) == True:
                # 更新
                self.ZMZManager.update_resource(res)
            else:
                self.ZMZManager.insert_resource(res)
            self.get_resource_prop(ul_li, res['Id']) # 解析属性
            self.ZMZLinkSpider.get_resource_base(html, res['Id']) # 解析资源code
        except Exception as e: 
            traceback.print_exc() # 打印错误代码行 
            pass
    
    # 获取资源属性
    def get_resource_prop(self, ul_li, resourceId):
        need = ['原名','地区','语言','首播','电视台','类型','别名']
        mult = ['编剧','編劇','导演','主演']
        if ul_li and len(ul_li) > 0:
            for li in ul_li:
                try:
                    prop = ResourceProp()
                    prop['ResourceId'] = resourceId
                    prop_name = ''
                    try:
                        prop_name = li.find('span').text.strip().rstrip('：').rstrip(':').strip()
                    except:
                        pass
                    prop['PropName'] = prop_name
                    if prop_name in need:
                        if prop_name == '别名':
                            prop['PropValue']  = li.text.replace('别名：','').strip()
                        else:
                            try:
                                prop['PropValue'] = li.find('strong').text.strip()
                            except:
                                prop['PropValue'] = ''
                        print('属性',prop)
                        self.ZMZManager.insert_resource_prop(prop)
                    elif prop_name in mult:
                        aa = li.find_all('a')
                        self.get_resource_character(prop_name, aa, resourceId)
                except Exception as e:            
                    logging.error(e)
                    pass    

    # 保存创作阵容
    def get_resource_character(self, prop_name, a_tags, resourceId):
        if a_tags and len(a_tags) > 0:
            for a in a_tags:
                # pdb.set_trace()
                href = a['href']
                cid = int(UrlTool.url_query_param(href,'character',default_value='',encoding='utf-8'))
                rc = ResourceCharacter()
                rc['ResourceId'] = resourceId
                rc['CharacterId'] = cid
                rc['CharacterType'] = prop_name
                print('资源角色', rc)
                self.ZMZManager.insert_resource_character(rc)
                c = Character()
                c['Id'] = cid
                c['NameCN'] = a.text.strip()
                c['NameEN'] = ''
                c['Url'] = href
                print('角色', c)
                self.ZMZManager.insert_character(c)


