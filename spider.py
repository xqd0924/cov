import json
import time
import sys
import traceback

import pymysql
import requests


def get_conn():
    conn = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='123',
                          db='cov',
                          charset='utf8')
    cursor = conn.cursor()
    return conn, cursor

def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def get_tencent_data():
    url_other = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }
    r = requests.get(url_other, headers)
    res = json.loads(r.text)
    data_all = json.loads(res['data'])

    history = {}
    for i in data_all['chinaDayList']:
        ds = "2020." + i['date']
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i['confirm']
        suspect = i['suspect']
        heal = i['heal']
        dead = i['dead']
        history[ds] = {'confirm': confirm, 'suspect': suspect, 'heal': heal, 'dead': dead}
    for i in data_all['chinaDayAddList']:
        ds = "2020." + i['date']
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i['confirm']
        suspect = i['suspect']
        heal = i['heal']
        dead = i['dead']
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    details = []
    url_h5 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    res_h5 = requests.get(url_h5, headers)
    d = json.loads(res_h5.text)
    data_h5 = json.loads(d['data'])
    update_time = data_h5['lastUpdateTime']
    data_country = data_h5['areaTree']
    data_province = data_country[0]['children']
    for pro_infos in data_province:
        province = pro_infos['name']
        for city_infos in pro_infos['children']:
            city = city_infos['name']
            confirm = city_infos['total']['confirm']
            confirm_add = city_infos['today']['confirm']
            heal = city_infos['total']['heal']
            dead = city_infos['total']['dead']
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    return history, details

def update_details():
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]
        conn, cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select %s=(select update_time from details order by id desc limit 1)"
        cursor.execute(sql_query, li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def insert_history():
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]
        print(f"{time.asctime()}开始插入历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            cursor.execute(sql, [k, v.get('confirm'), v.get('confirm_add'), v.get('suspect'),
                                v.get('suspect_add'), v.get('heal'), v.get('heal_add'),
                                v.get('dead'), v.get('dead_add')])
        conn.commit()
        print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_history():
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get('confirm'), v.get('confirm_add'), v.get('suspect'),
                                v.get('suspect_add'), v.get('heal'), v.get('heal_add'),
                                v.get('dead'), v.get('dead_add')])
        conn.commit()
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def get_baidu_hot():
    """
    :return: 返回百度疫情热搜
    """
    from selenium.webdriver import Chrome, ChromeOptions
    option = ChromeOptions()
    option.add_argument("--headless")  # 隐藏浏览器
    option.add_argument("--no-sandbox")

    url = "https://voice.baidu.com/act/virussearch/virussearch/?from=osari_aladin_news"
    browser = Chrome(options=option, executable_path="./chromedriver.exe")
    browser.get(url)
    btn = browser.find_element_by_css_selector(
        '#ptab-0 > div > div.VirusHot_1-5-6_32AY4F.VirusHot_1-5-6_2RnRvg > section > div')
    btn.click()  # 点击展开
    time.sleep(1)
    c = browser.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[1]/section/a/div/span[2]')
    context = [i.text for i in c]
    return context


def update_hotsearch():
    """
    将疫情热搜插入数据库
    :return:
    """
    cursor = None
    conn = None
    try:
        context = get_baidu_hot()
        print(f"{time.asctime()}开始更新热搜数据")
        conn, cursor = get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql, (ts, i))
        conn.commit()
        print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


if __name__ == '__main__':
    l = len(sys.argv)
    if l == 1:
        s = """
        ***请输入参数***
        参数说明：
        up_his  更新历史记录表
        up_hot  更新实时热搜
        up_det  更新详情表
        """
        print(s)
    else:
        order = sys.argv[1]
        if order == 'up_his':
            update_history()
        elif order == 'up_hot':
            update_hotsearch()
        elif order == 'up_det':
            update_details()