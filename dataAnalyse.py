import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dbUtils import DBUtils


# 加载数据库数据，绘制图形
def analyse_data():
    db = DBUtils()
    # 连接数据库
    db.db_connect()

    # 加载数据库中的指定数据
    db_query_data = db.db_get_info({'_id': 0, '建筑面积': 1, '房屋总价': 1, '装修情况': 1, '行政区域': 1})

    db.db_close()
    # 使用pandas将数据转为为数据集
    dataSet = pd.DataFrame(list(db_query_data))
    # print(dataSet)

    # 修改指定数据格式
    dataSet['建筑面积'] = dataSet['建筑面积'].str[:-1]

    # 将数据转为数组形式
    dataArr = np.array(dataSet)
    # 区域
    x_district = dataArr[:, 2]

    # 按区域分割数据集
    data_address1 = dataArr[x_district == '鼓楼', :]
    # 装修情况
    x1_decoration = data_address1[:, 3]

    # 按装修情况分割数据集
    dataset_address1_decoration = data_address1[x1_decoration == '毛坯', :]
    dataset_address2_decoration = data_address1[x1_decoration == '简装', :]
    dataset_address3_decoration = data_address1[x1_decoration == '精装', :]
    dataset_address4_decoration = data_address1[x1_decoration == '其他', :]
    # print(data_address1)

    # 面积与价格数据
    x1_area_d = dataset_address1_decoration[:, 0].astype('float')
    y1_price_d = dataset_address1_decoration[:, 1].astype('float')

    x2_area_d = dataset_address2_decoration[:, 0].astype('float')
    y2_price_d = dataset_address2_decoration[:, 1].astype('float')

    x3_area_d = dataset_address3_decoration[:, 0].astype('float')
    y3_price_d = dataset_address3_decoration[:, 1].astype('float')

    x4_area_d = dataset_address4_decoration[:, 0].astype('float')
    y4_price_d = dataset_address4_decoration[:, 1].astype('float')

    # 排序
    x1_sort = np.sort(x1_area_d)
    index = np.argsort(x1_area_d)
    y1_sort = [y1_price_d[i] for i in index]

    x2_sort = np.sort(x2_area_d)
    index = np.argsort(x2_area_d)
    y2_sort = [y2_price_d[i] for i in index]

    x3_sort = np.sort(x3_area_d)
    index = np.argsort(x3_area_d)
    y3_sort = [y3_price_d[i] for i in index]

    x4_sort = np.sort(x4_area_d)
    index = np.argsort(x4_area_d)
    y4_sort = [y4_price_d[i] for i in index]

    # print(x1_sort)

    # 绘图
    ax1 = plt.subplot2grid(shape=(2, 2), loc=(0, 0))
    ax1.scatter(x1_sort, y1_sort, s=10)
    ax1.set_ylabel('总价（万元）')
    ax1.set_xlabel('面积（平方米）')
    ax1.set_title('鼓楼区二手房-毛坯-建筑面积与房屋总价格关系图')

    ax2 = plt.subplot2grid(shape=(2, 2), loc=(0, 1))
    ax2.scatter(x2_sort, y2_sort, s=10)
    ax2.set_ylabel('总价（万元）')
    ax2.set_xlabel('面积（平方米）')
    ax2.set_title('鼓楼区二手房-简装-建筑面积与房屋总价格关系图')

    ax3 = plt.subplot2grid(shape=(2, 2), loc=(1, 0))
    ax3.scatter(x3_sort, y3_sort, s=10)
    ax3.set_ylabel('总价（万元）')
    ax3.set_xlabel('面积（平方米）')
    ax3.set_title('鼓楼区二手房-精装-建筑面积与房屋总价格关系图')

    ax4 = plt.subplot2grid(shape=(2, 2), loc=(1, 1))
    ax4.scatter(x4_sort, y4_sort, s=10)
    ax4.set_ylabel('总价（万元）')
    ax4.set_xlabel('面积（平方米）')
    ax4.set_title('鼓楼区二手房-其他-建筑面积与房屋总价格关系图')

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.subplots_adjust(hspace=0.6, wspace=0.5)
    plt.show()


if __name__ == '__main__':
    analyse_data()
