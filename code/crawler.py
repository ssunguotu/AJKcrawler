import requests
import pickle
import traceback
from bs4 import BeautifulSoup
import pickle
import time
import random
import os


# 存储pickle
def store_data(pkl, obj):
    try:
        with open(pkl, 'wb') as f:
            pickle.dump(obj, f)
        print('Data has been dumped into ' + pkl)
    except Exception as e:
        print('Save pickle failed due to ' + e)


# 加载pickle
def load_model(pkl):
    global cr
    if os.path.exists(pkl):
        print('load pickle object from ' + os.path.abspath(pkl))
        with open(pkl, 'rb') as f:
            cr = pickle.load(f)
        time.sleep(1)
    else:
        print('file not exits at ' + os.path.abspath(pkl))


# 存储一套房子信息的类
class HouseData(object):
    def __init__(self, type_, area, floor, buildTime, price):
        self.type = type_
        self.area = area
        self.floor = floor
        self.buildTime = buildTime
        self.price = price


# 爬虫
class Crawl(object):
    def __init__(self):
        # config
        self.url_base = 'https://xinxiang.anjuke.com/sale/'
        self.post_url = 'https://cloud-passport.anjuke.com/ajk/login/pc/dologin'
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.50',
            'referer':
            'https://login.anjuke.com/login/iframeform?style=1&forms=11&third_parts=111&other_parts=111&history=aHR0cHM6Ly94aW54aWFuZy5hbmp1a2UuY29tLw%3D%3D&check_bind_phone=1&t=1592494192942'
        }
        self.District = [
            'hongqibc/', 'weibina/', 'fengquanb/', 'muyeb/', 'weihuib/',
            'huixianb/', 'xinxiangxianb/', 'changyuanb/', 'fengqiu/',
            'huojia/', 'yanjin/', 'yuanyanga/', 'pingyuan/'
        ]

        # data
        self.data = {}
        for dist in self.District:  # 初始化存储的信息
            self.data[dist] = []

        # tmp data
        self.stopFlag = True
        self.url_iter = ''
        self.dist_iter = ''
        self.hasNxt = False
        self.cnt = 0
        pass

    def crawl(self):
        def getNxtInfo():  # 判断是否有下一页并获取下页的url
            soup.find_all(name='a', class_='aNxt')
            nxt = soup.find_all(name='a', class_='aNxt')
            assert len(nxt) <= 1
            if len(nxt) == 1:
                self.url_iter = nxt[0].get('href')
            else:
                self.hasNxt = False

        def getData():  # 得到房价的信息
            # 得到价格信息
            list_price = []
            for data_iter in soup.find_all(name='span', class_='price-det'):
                list_price.append(data_iter.find('strong').get_text())
            # 得到其他信息
            tmp = soup.find_all(name='div', class_='details-item')[::2]
            assert len(tmp) > 0 and len(tmp) == len(list_price)
            for i, data_iter in enumerate(tmp):
                msg = data_iter.get_text().strip().split('|')
                self.data[self.dist_iter].append(
                    HouseData(msg[0], msg[1], msg[2], msg[3], list_price[i]))

        try:
            for self.dist_iter in self.District[
                    self.District.index(self.dist_iter):]:  # 从dist_iter开始
                if not self.hasNxt:
                    self.url_iter = self.url_base + self.dist_iter  # + page
                self.hasNxt = True
                while self.hasNxt:  # 直到不存在下一页
                    html_doc = requests.get(url=self.url_iter,
                                            headers=self.headers).text
                    soup = BeautifulSoup(html_doc, 'lxml')
                    getNxtInfo()
                    getData()
                    time.sleep(random.randint(5, 10))  # 防止爬取过快
                    self.cnt += 1
                    print('dist:', self.dist_iter)
                    print('dataSize of this dist:',
                          len(self.data[self.dist_iter]))
                    print('已爬取次数:', self.cnt)
                    if cr.cnt % 20 == 0:
                        store_data(pkl, cr)  # 存储
                print('dist：%s 已抓取完成。' % self.dist_iter)
            self.stopFlag = True
            print('全部抓取完成。')

        # 如果有下一页，那么有class的名称为aNxt，否则没有class名称为aNxt。
        except KeyboardInterrupt:
            store_data(pkl, cr)  # 存储
            time.sleep(3)
            print('catch keyboard signal, exiting...')
            exit(0)

        except Exception as e:
            traceback.format_exc()
            print(str(e))


if __name__ == "__main__":
    pkl = 'crawl.pkl'
    cr = Crawl()
    if os.path.exists(pkl):
        load_model(pkl)  # 读取
    cr.crawl()
    print(cr.stopFlag)
