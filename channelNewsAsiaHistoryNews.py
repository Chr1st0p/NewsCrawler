import requests
from bs4 import BeautifulSoup
import mysql.connector
from utils.config import bcolors, DbConfig


class channelNewsAsia:
    url = 'http://www.channelnewsasia.com/archives/3636/Singapore/twoyears/latest/'

    def __init__(self):
        try:
            self.cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        except mysql.connector.Error as e:
            print bcolors.WARNING + 'connect fails!{}'.format(e) + bcolors.ENDC
        self.createTable()

    def start(self):
        for i in range(1000, -1, -1):
            self.getHtml(i)
        self.cnn.close()

    def getHtml(self, iters):
        targeturl = self.url + str(iters)
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        print 'Start Get ' + str(iters) + 'th Page TodayOnline News'
        html = requests.get(url=targeturl, headers=head)
        soup = BeautifulSoup(html.text, 'lxml')
        # delete the div with class=panel-panel right,
        # without this step, the result in next step will be class=panel-panel right + class=right;
        for div in soup.find_all("div", {'class': 'panel-panel right'}):
            div.decompose()

        # match the news div,the first one is the brief news which is useless,only 2-10 are the news;
        matchcontent = soup.find_all(name='div', attrs={'class', 'right'}, limit=11)

        # separete the title, link, date, abstract;
        for i in range(9, 0, -1):
            self.parseHtml(iters, matchcontent[i], i)

    def parseHtml(self, iters, match, i):
        # news title, link, date, abstract
        # noinspection PyBroadException
        try:
            title = match.find(name='h2').get_text()
        except:
            print bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th title Error' + bcolors.ENDC
            # print matchContent[i]
            title = ''
        # noinspection PyBroadException
        try:
            link = 'http://www.todayonline.com' + match.find(name='h2').find(name='a').get('href')
        except:
            print bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th link Error' + bcolors.ENDC
            link = ''
        # noinspection PyBroadException
        try:
            date = match.find(name='div', attrs={'class', 'timeago-highlight'}).get_text()
        except:
            print bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th date Error' + bcolors.ENDC
            date = ''
        # noinspection PyBroadException
        try:
            abstract = match.find(name='p').get_text()
            # abstract = matchContent[i].find(name='div', attrs={'class', 'class="article-abstract'}).get_text()
        except:
            print bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th abstract Error' + bcolors.ENDC
            abstract = ''
        data = (iters, title, link, date, abstract)
        self.insertData(data)

    def parserDebug(self, news):
        print news.find(name='h2').get_text()
        print news.find(name='h2').find(name='a').get('href')
        print news.find(name='div', attrs={'class', 'timeago-highlight'}).get_text()
        print news.find(name='p').get_text()

    def createTable(self):
        sqlCreateTable = "CREATE TABLE IF NOT EXISTS TodayHistoryNews (" \
                         "id       INT AUTO_INCREMENT PRIMARY KEY," \
                         "page     INT NOT NULL," \
                         "title    VARCHAR(1000) NOT NULL UNIQUE," \
                         "link     TEXT," \
                         "postdate     TEXT," \
                         "abstract TEXT)"

        cursor = self.cnn.cursor()
        try:
            cursor.execute(sqlCreateTable)
        except mysql.connector.Error as e:
            print bcolors.WARNING + 'create table TodayHistoryNews fails!{}'.format(e) + bcolors.ENDC

    def insertData(self, data):
        cursor = self.cnn.cursor()
        sql_insert = 'INSERT INTO TodayHistoryNews (page, title, link, postdate, abstract) VALUES (%s, %s, %s, %s, %s)'
        try:
            cursor.execute(sql_insert, data)
        except mysql.connector.Error as e:
            print bcolors.WARNING + 'insert data error!{}'.format(e) + bcolors.ENDC
        finally:
            self.cnn.commit()
            cursor.close()
