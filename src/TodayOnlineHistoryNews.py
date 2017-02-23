from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import mysql.connector
from utils.config import bcolors, DbConfig, requestHeader
import multiprocessing


def start():
    # max page 2357
    for i in range(2356, -1, -1):
        getHtml(i)
    TodayNews.cnn.close()


def getHtml(iters):
    if iters == 0:
        targeturl = TodayNews.url
    else:
        targeturl = TodayNews.url + TodayNews.pageDownStr + str(iters)
    print('Start Get ' + str(iters) + 'th Page TodayOnline News')
    html = requests.get(url=targeturl, headers=requestHeader.browserHeader)
    soup = BeautifulSoup(html.text, 'lxml')
    # delete the div with class=panel-panel right,
    # without this step, the result in next step will be class=panel-panel right + class=right;
    for div in soup.find_all("div", {'class': 'panel-panel right'}):
        div.decompose()

    # match the news div,the first one is the brief news which is useless,only 2-10 are the news;
    matchcontent = soup.find_all(name='div', attrs={'class', 'right'}, limit=11)
    print("whole match")
    print(matchcontent)
    poolToday = multiprocessing.Pool(processes=10)
    # separete the title, link, date, abstract;
    # print matchcontent[1]
    if len(matchcontent) >= 10:
        poolToday = multiprocessing.Pool(processes=10)
        for i in range(9, -1, -1):
            print('part match')
            print(matchcontent[i])
            poolToday.apply_async(parseHtml, args=(iters, matchcontent[i], i))

            # parseHtml(iters, matchcontent[i], i)
    else:
        poolToday = multiprocessing.Pool(processes=len(matchcontent))
        for i in range(len(matchcontent) - 1, -1, -1):
            print('part match')
            print(matchcontent[i])
            poolToday.apply_async(parseHtml, args=(iters, matchcontent[i], i))
    poolToday.close()
    poolToday.join()


def parseHtml(iters, match, i):
    # news title, link, date, abstract
    # noinspection PyBroadException
    matchlink = ''
    try:
        title = match.find(name='h2').get_text()
    except:
        print(bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th title Error' + bcolors.ENDC)
        title = ''
    print(title)
    # noinspection PyBroadException
    try:
        matchlink = match.find(name='h2').find(name='a').get('href')
        link = 'http://www.todayonline.com' + matchlink
    except:
        print(bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th link Error' + bcolors.ENDC)
        link = ''
    print(matchlink)
    content = ''
    if matchlink:
        contentHtml = requests.get(url=link, headers=requestHeader.browserHeader)
        contentSoup = BeautifulSoup(contentHtml.text, 'lxml')
        contentDiv = contentSoup.find_all(name='div', attrs={'class': 'content'})[0]
        contenP = contentDiv.find_all(name='p')
        for i in range(len(contenP)):
            content += contenP[i].get_text()
    # noinspection PyBroadException
    print(content)
    try:
        date = match.find(name='div', attrs={'class', 'timeago-highlight'}).get_text()
    except:
        print(bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th date Error' + bcolors.ENDC)
        date = ''
    print(date)
    # noinspection PyBroadException
    # try:
    #     abstract = match.find(name='p').get_text()
    #     # abstract = matchContent[i].find(name='div', attrs={'class', 'class="article-abstract'}).get_text()
    # except:
    #     print bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th abstract Error' + bcolors.ENDC
    #     abstract = ''

    # data = (iters, title, link, date, content)
    # if title and matchlink and date and ('TODAY\'s morning brief' not in title):
    #     insertData(data)


def parserDebug(news):
    print(news.find(name='h2').get_text())
    print(news.find(name='h2').find(name='a').get('href'))
    print(news.find(name='div', attrs={'class', 'timeago-highlight'}).get_text())
    print(news.find(name='p').get_text())


def createTable():
    sqlCreateTable = "CREATE TABLE IF NOT EXISTS todayonline (" \
                     "id       INT AUTO_INCREMENT PRIMARY KEY," \
                     "page     INT NOT NULL," \
                     "title    VARCHAR(1000) NOT NULL UNIQUE," \
                     "link     TEXT," \
                     "postdate     TEXT," \
                     "content TEXT)"

    cursor = TodayNews.cnn.cursor()
    try:
        cursor.execute(sqlCreateTable)
    except mysql.connector.Error as e:
        print(bcolors.WARNING + 'create table todayonline fails!{}'.format(e) + bcolors.ENDC)


def insertData(data):
    cursor = TodayNews.cnn.cursor()
    # sql_insert = 'INSERT INTO todayonline (page, title, link, postdate,content) VALUES (%s, %s, %s, %s, %s)'
    sql_insert = 'INSERT INTO todayonline (page, title, link, postdate, content) VALUES (%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql_insert, data)
    except mysql.connector.Error as e:
        print(bcolors.WARNING + 'insert data error!{}'.format(e) + bcolors.ENDC)
    finally:
        TodayNews.cnn.commit()
        cursor.close()


class TodayNews:
    url = 'http://www.todayonline.com/singapore'
    pageDownStr = '?page='
    cnn = mysql.connector.connect(**DbConfig.newsDataConfig)

    def __init__(self):
        # try:
        #     self.cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        # except mysql.connector.Error as e:
        #     print bcolors.WARNING + 'connect fails!{}'.format(e) + bcolors.ENDC
        createTable()
