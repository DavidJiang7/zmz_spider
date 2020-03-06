from selenium import webdriver
import pdb, random, time, traceback

class WebSelenium():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--ignore-certificate-errors')  # 忽略证书验证错误
        options.add_extension('F:\\py\\zmz_spider\\utils\\AdblockPlus2.crx') # 安装屏蔽广告插件
        options.add_argument("--user-data-dir="+"F:\\py\\zmz_spider\\utils\\User Data") # 加载用户缓存信息
        self.driver = webdriver.Chrome('F:\\py\\zmz_spider\\utils\\chromedriver.exe', options = options)
        # self.driver.implicitly_wait(3) # 只等待页面10秒
        # self.driver.set_page_load_timeout(10) # 页面加载等待超时

    def get_html(self, url):
        try:
            return self.get(url)
        except Exception as e: 
            print(e)
            traceback.print_exc() # 打印错误代码行           
            secends = random.randint(300, 600)
            print('第一次 出现异常，休息一会儿......')
            print(str(secends) + '秒后继续')
            time.sleep(secends)   # 暂停5~10分钟，然后再尝试一次
            try:
                return self.get(url)
            except Exception as ex: 
                print(ex)
                traceback.print_exc() # 打印错误代码行 
                print('第二次 出现异常，休息一会儿......')
                print('30分钟后继续')
                time.sleep(600)   # 暂停10分钟
                return ''

    def get(self, url):
        self.driver.get(url)
        self.driver.find_element_by_xpath('//head') #尝试找html标签
        return self.driver.page_source


