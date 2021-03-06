import time
import pymysql


def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format('年', '月', '日')

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

def query(sql, *args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，((),(),)形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res

def get_c1_data():
    """
    :return: 返回大屏的统计数据
    """
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal)," \
          "sum(dead) " \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1)"
    res = query(sql)
    return res[0]

def get_c2_data():
    """
    :return: 返回各省数据
    """
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res

def get_le1_data():
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res

def get_le2_data():
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res

def get_r_data():
    """
    :return: 返回非湖北地区城市确诊前5名
    """
    sql = "select city,confirm from " \
          "(select city,confirm from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) " \
          "and province not in ('湖北','北京','上海','天津','重庆')" \
          "union all " \
          "select province as city,sum(confirm) as confirm from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) " \
          "and province in ('北京','上海','天津','重庆') group by province) as a " \
          "order by confirm desc limit 5"
    res = query(sql)
    return res

def get_r1_data():
    """
    :return: 返回现有确诊省市top5
    """
    sql = "SELECT province,(SUM(confirm)-SUM(heal)-SUM(dead)) AS new FROM details " \
          "WHERE update_time=(SELECT update_time FROM details ORDER BY update_time DESC LIMIT 1) " \
          "GROUP BY province ORDER BY new DESC LIMIT 5;"
    res = query(sql)
    return res

def get_r2_data():
    """
    :return: 返回最近的20条热搜
    """
    sql = 'select content from hotsearch order by id desc limit 20'
    res = query(sql)
    return res

if __name__ == '__main__':
    print(get_r1_data())