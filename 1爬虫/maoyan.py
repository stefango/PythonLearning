# 导入标准库模块
import json

# 导入第三方模块
# CMD中pip install requests、pip install lxml
import requests
from lxml import etree


def getOnePage(pageNum):

    # 字符串的格式化方法之一
    url = f'http://maoyan.com/board/4?offset={pageNum*10}'

    # 告诉服务器 我是浏览器
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}

    # 返回Response
    r = requests.get(url, headers=header)

    # 输出http状态码200
    print(r)

    return r.text


def parse(text):

    html = etree.HTML(text)
    name_list = html.xpath(
        '//div[@class="movie-item-info"]/p[@class="name"]/a/@title')
    release_time_list = html.xpath('//p[@class="releasetime"]/text()')

    # print(name_list)
    # print(release_time_list)

    # 字典
    item = {}  # 或者item = dict()

    # 拉链函数zip
    for name, release_time in zip(name_list, release_time_list):
        item['name'] = name
        item['release_time'] = release_time
        # 生成器 循环迭代
        yield item
        # print(name,release_time)


def save2File(data):
    with open('movies.json', 'a', encoding='utf-8') as f:
        # dumps()把字典、列表转化为字符串
        data = json.dumps(data, ensure_ascii=False) + ',\n'
        f.write(data)


def run(start, end):
    for n in range(start, end):

        text = getOnePage(n)

        items = parse(text)

        for item in items:
            print(item)
            save2File(item)


if __name__ == '__main__':

    run(0, 10)