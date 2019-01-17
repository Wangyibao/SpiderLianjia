import requests
from lxml import etree
import time
from dbUtils import DBUtils
from multiprocessing import Pool

# 加入请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
    'Connection': 'close'}

# 创建数据库工具类
db = DBUtils()

# 数组，存放每页数据
# list_page_info = []

# 标志，是否第一次爬取数据
flag_first_access = True
# 存放基本属性名称
list_basic_attribute_name = []


def get_sub_links(url):
    try:
        res = requests.get(url, headers=headers, timeout=2)
    except (requests.Timeout, requests.ConnectTimeout,):
        print("网络连接失败")
        return
    except requests.exceptions.ConnectionError:
        print("网络连接错误，需要休息。。。")
        time.sleep(3)
        return

    selector = etree.HTML(res.text)
    # 获取详情页urls
    sub_links = selector.xpath('/html/body/div[4]/div[1]/ul/li/div[1]/div[1]/a/@href')
    for sub_link in sub_links:
        print('详情地址：', sub_link)
        # 获取详情页的数据
        get_info(sub_link)
        # dict_item = get_info(sub_link)
        # 将数据放入数组中
        # list_page_info.append(dict_item)
        # 睡眠0.5s，防止访问过快
        time.sleep(0.5)
    # 插入一页数据
    # data_process(list_page_info)
    return


def get_info(url):
    # 声明为全局变量
    global flag_first_access, list_basic_attribute_name
    # dict,存放爬取的数据
    dict_house_info = {}

    try:
        res = requests.get(url, headers=headers, timeout=2)
    except (requests.Timeout, requests.ConnectTimeout):
        print("网络连接异常")
        return
    except requests.exceptions.ConnectionError:
        print("网络连接错误，需要休息。。。")
        time.sleep(3)
        return

    selector = etree.HTML(res.text)

    try:
        if flag_first_access:
            flag_first_access = False
            # 获取基本属性名称，并放入数组
            list_basic_attribute_name = selector.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul')[0].xpath(
                'li/span/text()')

        # 数组，存放基本属性值
        list_basic_attribute_value = selector.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul')[0].xpath(
            'li/text()')

        dict_house_info['标题名称'] = selector.xpath('/html/body/div[3]/div/div/div[1]/h1/text()')[0]
        dict_house_info['房屋总价'] = selector.xpath('/html/body/div[5]/div[2]/div[2]/span[1]/text()')[0]
        dict_house_info['小区名称'] = selector.xpath('/html/body/div[5]/div[2]/div[4]/div[1]/a[1]/text()')[0]
        dict_house_info['行政区域'] = selector.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/span[2]/a[1]/text()')[0]
        dict_house_info['房屋地址'] = selector.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/span[2]/a[2]/text()')[0]
    except IndexError:
        pass

    for k, v in zip(list_basic_attribute_name, list_basic_attribute_value):
        dict_house_info[k] = v

    # 打印爬取的内容
    for k, v in dict_house_info.items():
        print(k, ':', v)

    # 插入单个数据
    data_process(dict_house_info)
    return dict_house_info


def data_process(info):
    # 连接数据库
    db.db_connect()

    db.db_insert_one(info)

    db.db_close()

    return


if __name__ == '__main__':
    urls = ['https://nj.lianjia.com/ershoufang/pg{}sf1//'.format(num) for num in range(1, 40)]

    # 单进程
    # for url in urls:
    #     print(url)
    #     # 获得爬取数据的详细url
    #     get_sub_links(url)

    # 多进程
    start_time = time.time()
    pool = Pool(processes=3)
    pool.map(get_sub_links, urls)
    end_time = time.time()
    print('运行时间：', end_time - start_time)

    # 测试
    # url = 'https://nj.lianjia.com/ershoufang/103102604811.html'
    # get_info(url)
