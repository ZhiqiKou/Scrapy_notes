# -*- coding: utf-8 -*-

import json
import redis
import pymysql

def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    # 指定mysql数据库
    mysqlcli = pymysql.connect(host='127.0.0.1', user='root', passwd='zhiqi', db='Scrapy', port=3306, use_unicode=True)

    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["dytt_slaver:items"])
        item = json.loads(data)

        try:
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            # 使用execute方法执行SQL INSERT语句
            cur.execute("INSERT INTO dytt (name, year, language, "
                        "movie_type, release_date, score, file_size, "
                        "film_time, introduction, posters, download_link) VALUES "
                        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )",
                        [item['name'], item['year'], item['language'],
                         item['movie_type'], item['release_date'], item['score'],
                         item['file_size'], item['film_time'], item['introduction'],
                         item['posters'], item['download_link']])
            # 提交sql事务
            mysqlcli.commit()
            #关闭本次操作
            cur.close()
            print ("inserted %s" % item['name'])
        except pymysql.Error as e:
            print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))


if __name__ == '__main__':
    main()