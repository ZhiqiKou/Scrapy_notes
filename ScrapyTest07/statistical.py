from pyecharts import Bar
from pyecharts import Line
from pyecharts import WordCloud
from pyecharts import Geo
from pyecharts import Pie
from pyecharts.engine import create_default_environment
import pymysql
import jieba
import re

db = pymysql.connect(host='localhost', user='root', password='zhiqi', database='Scrapy')
cursor = db.cursor()

sql = "SELECT * FROM my_qzone"

contents = []
years = []
months = []
days = []
hours = []
locations = {}
source_names = []

try:
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        contents.append(row[1])
        years.append(row[2].split(' ')[0].split('-')[0])
        months.append(row[2].split(' ')[0].split('-')[1])
        days.append(row[2].split(' ')[0].split('-')[2])
        hours.append(row[2].split(' ')[1].split(':')[0])
        locations[row[3]] = [row[4], row[5]]
        if row[6] != '':
            source_names.append(row[6])
except Exception as e:
    # 输出错误信息
    print(e)

cursor.close()
db.close()


# 将所有说说连起来
str_content = ''
for content in contents:
    str_content += content
str_content = ''.join(re.findall(u'[\u4e00-\u9fff]+', str_content))
words = jieba.cut(str_content)
stop_list = ['的', '了', '我', '是', '不',
             '你', '都', '就', '在', '也',
             '有', '去', '好', '说', '到',
             '又', '要', '这', '还', '啊',
             '吧', '给', '和', '人', '来',
             '被', '上', '没', '会', '能',
             '着', '多', '他', '一', '年',
             '看', '很', '谁', '再', '为',
             ]
result_word_list = []
for word in words:
    if word not in stop_list:
        result_word_list.append(word)

geo = Geo(
    "位置信息",
    title_color="#fff",
    title_pos="center",
    width=1200,
    height=600,
    background_color="#404a59",
)

sorted_list = set(list(locations.keys()))
list_infos = {}
for info in sorted_list:
    list_infos[info] = list(locations.keys()).count(info)

attr, value = geo.cast(list_infos)
geo.add(
    "",
    attr,
    value,
    geo_cities_coords=locations
)
geo.render()


def get_chart(original_list, form_type, table_name, series_name):
    sorted_list = sorted(list(set(original_list)))
    list_infos = {}
    for info in sorted_list:
        list_infos[info] = original_list.count(info)
    chart = form_type(table_name)
    chart.add(series_name, list(list_infos.keys()), list(list_infos.values()))
    return chart


def drawing(chart, path, filet_type='html'):
    env = create_default_environment(filet_type)
    # create_default_environment(filet_type)
    # file_type: 'html', 'svg', 'png', 'jpeg', 'gif' or 'pdf'
    env.render_chart_to_file(chart, path=path)

drawing(get_chart(years, Bar, '年发表统计图', '发表数'), 'years.html')
drawing(get_chart(months, Bar, '月发表统计图', '发表数'), 'months.html')
drawing(get_chart(days, Bar, '日发表统计图', '发表数'), 'days.html')
drawing(get_chart(hours, Bar, '小时发表统计图', '发表数'), 'hours.html')
drawing(get_chart(result_word_list, WordCloud, '', ''), 'word.html')
drawing(get_chart(source_names, Pie, '', ''), 'source.html')
