import time, pdb, random, json, datetime
from storage.manager import ZMZManager
from utils.http import UrlTool, Http

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
                        # 0-未更新json，1-完成解析，2-正在解析json，3-解析json异常，4-被屏蔽拿不到json， 5-404
                        self.ZMZManager.update_resource_base_status(res['Id'], 4)   # 被屏蔽，可重试
                        continue
                    self.get_link(res, html)
                    secends = random.randint(1, 10)
                    time.sleep(secends)
            if len(resources) < pageSize:
                break 
    
    # 获取每集基础信息
    def get_link(self, data, html):
        result = json.loads(html)
        if result['status'] == 404:
            print('http status: 404, resouceId:', data['Id'])
            self.ZMZManager.update_resource_base_status(data['Id'], 5)   # 404
            return
        # pdb.set_trace()
        if result['status'] == 1 and 'data' in result and 'info' in result['data'] and 'list' in result['data']:
            info = result['data']['info']
            items = result['data']['list']
            # 更新base信息
            data['NameCN'] = info.get('cnname', '')
            data['NameEN'] = info.get('enname', '')
            data['OtherName'] = info.get('aliasname', '')
            data['Channel'] = info.get('channel', '')
            data['ChannelCN'] = info.get('channel_cn', '')
            data['Area'] = info.get('area', '')
            data['ShowType'] = info.get('show_type', '')
            data['Views'] = info.get('views', 0)
            data['Status'] = 2 # 正在解析json
            data['UpdateTime'] = datetime.datetime.now()
            data['LinkJson'] = json.dumps(items)
            print('资源id：', data['Id'], '开始...')
            self.get_episode_link(html)
            self.ZMZManager.update_resource_base(data)
            print('资源id：', data['Id'], '结束...')

    # 获取下载链接
    def get_episode_link(self, html):
        result = json.loads(html)
        if 'data' in result and 'info' in result['data'] and 'list' in result['data']:
            info = result['data']['info']
            items = result['data']['list']
            for item in items:
                season_cn = item['season_cn']
                season_num = item['season_num']
                for f in item['formats']:
                    for episode in item['items'][f]:
                        epi = {}
                        epi['EpisodeId'] = episode['itemid']
                        epi['ResourceId'] = info['id']
                        epi['SeasonCN'] = season_cn
                        epi['SeasonNum'] = season_num
                        epi['Formats'] = f
                        epi['Episode'] = episode['episode']
                        epi['FileName'] = episode['name']
                        epi['FileSize'] = episode['size']
                        try:                        
                            # print(epi)    
                            self.ZMZManager.insert_data(epi, 'ResourceEpisode') 
                        except:
                            print('可能重复插入记录，可忽略...')
                            pass
                        if episode['files'] is not None:
                            for fi in episode['files']:
                                link = {}
                                link['ResourceId'] = info['id']
                                link['EpisodeId'] = episode['itemid']
                                link['Way'] = fi['way']
                                link['WayCN'] = fi['way_cn']
                                link['Url'] = fi['address']
                                link['Password'] = fi['passwd']
                                self.ZMZManager.insert_data(link, 'ResourceEpisodeLink') 
                                # print(link)
                                
