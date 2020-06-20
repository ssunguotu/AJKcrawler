'''
goal:
1. 在售二手房的房源数量  : 柱状图
2. 在售房源的平均售价
3. 平均单价（每平方米的价格） ： 柱状图
4. 在售房源分布图
6. 价格区间柱状图
7. 在售房源按区域划分的价格图
'''
import pickle
import os
import time
from crawler import HouseData, Crawl
from matplotlib import pyplot as plt
from matplotlib import rcParams

cr = Crawl()  # Crawl
pkl = 'crawl.pkl'
name_mp = {
    'hongqibc/': '红旗区',
    'weibina/': '卫滨区',
    'fengquanb/': '凤泉区',
    'muyeb/': '牧野区',
    'weihuib/': '卫辉市',
    'huixianb/': '辉县市',
    'xinxiangxianb/': '新乡县',
    'changyuanb/': '长垣县',
    'fengqiu/': '封丘县',
    'huojia/': '获嘉县',
    'yanjin/': '延津县',
    'yuanyanga/': '原阳县',
    'pingyuan/': '平原示范区'
}


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


class Data(object):
    def __init__(self):

        self.list_houseNum = {}  # 各区域房源数量
        self.sum_houseNum = 0  # 房源总数
        self.sum_averagePrice = 0  # 总平均房价
        self.list_averagePrice = {}  # 各区域的平均房价,key为区域，value为平均房价房价

        for dist in cr.District:
            self.list_houseNum[dist] = 0
            self.list_averagePrice[dist] = 0

    def getData(self):
        # area:'136m²'  buildTime:'2000年建造' price:'高层(共6层)' type:'45''4室2厅'
        sum_allhousePrice = 0
        for dist in cr.District:
            self.list_houseNum[dist] = len(cr.data[dist])  # 各区域房源数量
            sum_housePrice = 0
            for house in cr.data[dist]:  # list
                sum_housePrice += float(house.price) / float(house.area[:-2])

            self.list_averagePrice[dist] = sum_housePrice / self.list_houseNum[
                dist]  # 各区域的平均房价
            sum_allhousePrice += sum_housePrice  # 所有房子的总价格
            self.sum_houseNum += len(cr.data[dist])  # 房子的总数
        self.sum_averagePrice = sum_allhousePrice / self.sum_houseNum  # 房子的总均价


load_model(pkl)
d = Data()
d.getData()
# 画图
# 房源分布饼状图
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False
label_list = [name_mp[dist] for dist in cr.District]  # 各部分标签
size = [d.list_houseNum[dist] for dist in cr.District]  # 各部分大小
# color = ["r", "g", "b"]  # 各部分颜色
# explode = [0.05, 0, 0]  # 各部分突出值
patches, l_text, p_text = plt.pie(size,  labels=label_list, labeldistance=1.1, autopct="%1.1f%%", shadow=True, startangle=90, pctdistance=0.6)
plt.axis("equal")    # 设置横轴和纵轴大小相等，这样饼才是圆的
plt.title("饼状图")
plt.legend()
plt.show()

# 房价柱状图
# 生成画布
plt.figure(figsize=(12, 6), dpi=80)
# 横坐标
label_list = [name_mp[dist] for dist in cr.District]  # 各部分标签
# 纵坐标
y = [d.list_averagePrice[dist] * 10000 for dist in cr.District]
x = range(len(label_list))

plt.bar(x, y, width=0.5)
plt.xticks(x, label_list)
plt.show()
