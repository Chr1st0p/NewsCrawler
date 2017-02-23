from __future__ import print_function
import requests
import multiprocessing
from bs4 import BeautifulSoup
import mysql.connector
from utils.config import bcolors, DbConfig, requestHeader
import re


def main():
    for i in range(94, -1, -1):
        getHtml(i)
    StraitsTimesNews.cnn.close()


def getHtml(iters):
    if iters == 0:
        targeturl = StraitsTimesNews.url
    else:
        targeturl = StraitsTimesNews.url + StraitsTimesNews.pageDownStr + str(iters)
    print('Start Get ' + str(iters) + 'th Page StraitsTimes News')
    html = requests.get(url=targeturl, headers=requestHeader.browserHeader)
    soup = BeautifulSoup(html.text, 'lxml')

    matchTittleLink = soup.find_all(name='div', attrs={'class', 'media-body '})
    matchDate = soup.find_all(name='div', attrs={'class', 'media-footer'})
    # if len(matchTittleLink) == 0:
    #     pool2 = multiprocessing.Pool(processes=25)
    # else:
    pool2 = multiprocessing.Pool(processes=27)
    # separete the title, link, date
    for i in range(len(matchDate) - 1, -1, -1):
        # pool.map()
        pool2.apply_async(parseHtml, args=(iters, matchTittleLink[i], matchDate[i], i))
        # parseHtml(iters, matchTittleLink[i], matchDate[i], i)
        # self.paraseNews(matchTittleLink[i], matchDate[i])
    pool2.close()
    pool2.join()
    # print 'get ' + str(iters) + 'th page done'


def paraseNewsDebug(TitLink, Date):
    try:
        print(TitLink.find(name='a').get_text())
    except:
        print("None Title Match")
    try:
        print(TitLink.find(name='a').get('href'))
    except:
        print("None Link Match")
    try:
        print(Date.find(name='div', attrs={'class', 'node-postdate'}).get_text())
    except:
        print("None Date Match")


def parseHtml(iters, matchTL, matchD, i):
    # news title, link, date,
    # noinspection PyBroadException
    # print 'start'
    try:
        title = matchTL.find(name='a').get_text()
    except:
        print(bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th title Error' + bcolors.ENDC)
        title = ''
    # noinspection PyBroadException
    try:
        link = 'http://www.straitstimes.com' + matchTL.find(name='a').get('href')
    except:
        print(bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th link Error' + bcolors.ENDC)
        link = ''

    # noinspection PyBroadException
    if link == '':
        content = ''
        keyword = ''
    else:
        # noinspection PyBroadException
        try:
            keyword, content = parseContentKeyword(link)
        except:
            keyword = ''
            content = ''
            print("No key word or content matches")

    # noinspection PyBroadException
    try:
        date = matchD.find(name='div', attrs={'class', 'node-postdate'}).get_text()
    except:
        print(bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th date Error' + bcolors.ENDC)
        date = ''
    data = (iters, title, link, date, keyword, content)
    if keyword:
        insertData(data)


def insertData(data):
    cursor = StraitsTimesNews.cnn.cursor()
    sql_insert = 'INSERT INTO StraitsTimesHistoryNews (page, title, link, postdate,keyword,content) VALUES (%s, %s, %s, %s,%s,%s)'
    try:
        cursor.execute(sql_insert, data)
    except mysql.connector.Error as e:
        print(bcolors.WARNING + 'insert data error!{}'.format(e) + bcolors.ENDC)
    finally:
        StraitsTimesNews.cnn.commit()
        cursor.close()


def parseContentKeyword(newsurl):
    html = requests.get(url=newsurl, headers=requestHeader.browserHeader)
    try:
        keyword = re.findall(r".*\"keyword\":\"(.*?)\",.*", html.text)
        soup = BeautifulSoup(html.text, 'lxml')
        matchContent = soup.find_all(name='p')
    except:
        print("Keyword or content match Error")
        return '', ''
    content = ''
    for i in range(len(matchContent) - 5):
        content += matchContent[i].get_text()
    return keyword[0], content


def createTable():
    sqlCreateTable = "CREATE TABLE IF NOT EXISTS StraitsTimesHistoryNews (" \
                     "id       INT AUTO_INCREMENT PRIMARY KEY," \
                     "page     INT NOT NULL," \
                     "title    VARCHAR(1024) UNIQUE," \
                     "link     TEXT," \
                     "postdate TEXT," \
                     "keyword TEXT," \
                     "content TEXT)"
    cursor = StraitsTimesNews.cnn.cursor()
    try:
        cursor.execute(sqlCreateTable)
    except mysql.connector.Error as e:
        print(bcolors.WARNING + 'create table StraitsTimesHistoryNews fails!{}'.format(e) + bcolors.ENDC)


class StraitsTimesNews:
    cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
    url = 'http://www.straitstimes.com/singapore/latest'
    pageDownStr = '?page='


    def __init__(self):
        # try:
        #     cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        # except mysql.connector.Error as e:
        #     print bcolors.WARNING + 'connect fails!{}'.format(e) + bcolors.ENDC
        createTable()
