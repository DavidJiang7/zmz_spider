from urllib import parse
import re, requests, random, json

USER_AGENT_LIST = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/5.0 Opera 11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20130514 Firefox/21.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
]

COOKIES = [
    "sitefrom=2c009307000452003fe3557fb8185917d; NTKF_T2D_CLIENTID=guestACD55A50-AE29-8E8A-E69B-F7E971BA62EB; miyaid=vcrg8fogq558d6vvlfp116smc2; Hm_lvt_cb6c9083cb8f4836bf3087e80ab885b0=1576117254,1576217101; Hm_lvt_d2cf6545e0ff1d556245dafeb1e76ed6=1576217132; scan_sku=4538065,4538063,5089763,4558170,5159353; nTalk_CACHE_DATA={uid:hw_1000_ISME9754_getcookie(|miauid|),tid:1576220449181070}; item_size=SINGLE; WT_FPC=id=218fb8fbae6820541c51576117242343:lv=1576220483315:ss=1576217099665:lsv=1576127197614:vs=1:spv=44; Hm_lpvt_d2cf6545e0ff1d556245dafeb1e76ed6=1576220483; Hm_lpvt_cb6c9083cb8f4836bf3087e80ab885b0=1576220483",
]

class Http():
     
    def get_html(self, url):
        try:
            return self.__request(url)
        except:            
            traceback.print_exc() # 打印错误代码行
            print('出现异常，休息一会儿......')
            time.sleep(random.randint(600, 1800))   # 暂停10~30分钟，然后再尝试一次
            try:
                print('重试请求......')
                return self.__request(url)
            except:
                print('出现异常，休息一会儿......')
                time.sleep(1800)   # 暂停30分钟
                return ''

                
    def __request(self, url):
        headers = {
            'User-Agent': random.choice(USER_AGENT_LIST),
            'Cookie': random.choice(COOKIES),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        response = requests.get(url, headers=headers)
        response.encoding ='utf-8'
        return response.text




class UrlTool(object):

    @staticmethod
    def url_query_replace(url:str,key:str,val:str,encoding='utf-8') -> str:
        """
        替换某个参数值
        """
        start_uri = parse.urlparse(url)
        key = str(key)
        val = str(val)
        qs = parse.parse_qs(start_uri.query,keep_blank_values=True,encoding=encoding)
        qs[key]=(str(val),)
        new_query ='&'.join(map(lambda x :'{0}={1}'.format(x,parse.quote(qs[x][0],encoding=encoding)),qs))
        return parse.urlunparse((start_uri.scheme,start_uri.netloc,start_uri.path,start_uri.params,new_query,start_uri.fragment))
    
    @staticmethod
    def url_query_param(url:str,key:str,*,default_value:str='',encoding='utf-8') -> str:
        """
        获取链接中某个参数的值
        """
        key = str(key)
        default_value = str(default_value)
        start_uri = parse.urlparse(url)
        qs = parse.parse_qs(start_uri.query,keep_blank_values=True,encoding=encoding)
        param_value = qs.get(key)
        if param_value is None:
            return default_value
        return param_value[0]    

    @staticmethod
    def url_query_remove(url:str,key:str,encoding='utf-8') -> str:
        start_uri = parse.urlparse(url)
        key = str(key)
        qs = parse.parse_qs(start_uri.query,keep_blank_values=True,encoding=encoding)
        if key in qs.keys():
            qs.pop(key)
        new_query ='&'.join(map(lambda x :'{0}={1}'.format(x,parse.quote(qs[x][0],encoding=encoding)),qs))
        return parse.urlunparse((start_uri.scheme,start_uri.netloc,start_uri.path,start_uri.params,new_query,start_uri.fragment))
