import requests
from bs4 import BeautifulSoup
import mysql.connector
from utils.config import bcolors, DbConfig
import re


class straitsTimesNews:
    url = 'http://www.straitstimes.com/singapore/latest'
    pageDownStr = '?page='

    def __init__(self):
        try:
            self.cnn = mysql.connector.connect(**DbConfig.newsDataConfig)
        except mysql.connector.Error as e:
            print bcolors.WARNING + 'connect fails!{}'.format(e) + bcolors.ENDC
        self.createTable()

    def start(self):
        for i in range(2, -1, -1):
            self.getHtml(i)
        self.cnn.close()

    def getHtml(self, iters):
        if iters == 0:
            targeturl = self.url
        else:
            targeturl = self.url + self.pageDownStr + str(iters)
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        print 'Start Get ' + str(iters) + 'th Page StraitsTimes News'
        html = requests.get(url=targeturl, headers=head)
        soup = BeautifulSoup(html.text, 'lxml')

        matchTittleLink = soup.find_all(name='div', attrs={'class', 'media-body '})
        matchDate = soup.find_all(name='div', attrs={'class', 'media-footer'})

        # separete the title, link, date
        for i in range(len(matchDate) - 1, -1, -1):
            self.parseHtml(iters, matchTittleLink[i], matchDate[i], i)
            # self.paraseNews(matchTittleLink[i], matchDate[i])

    def paraseNewsDebug(self, TitLink, Date):
        try:
            print TitLink.find(name='a').get_text()
        except:
            print "None Title Match"
        try:
            print TitLink.find(name='a').get('href')
        except:
            print "None Link Match"
        try:
            print Date.find(name='div', attrs={'class', 'node-postdate'}).get_text()
        except:
            print "None Date Match"

    def parseHtml(self, iters, matchTL, matchD, i):
        # news title, link, date,
        # noinspection PyBroadException
        try:
            title = matchTL.find(name='a').get_text()
        except:
            print bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th title Error' + bcolors.ENDC
            title = ''
        # noinspection PyBroadException
        try:
            link = 'http://www.straitstimes.com' + matchTL.find(name='a').get('href')
        except:
            print bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th link Error' + bcolors.ENDC
            link = ''

        # noinspection PyBroadException
        if link == '':
            content = ''
            keyword = ''
        else:
            # noinspection PyBroadException
            try:
                keyword, content = self.parseContentKeyword(link)
            except:
                keyword = ''
                content = ''
                print "No key word or content matches"

        # noinspection PyBroadException
        try:
            date = matchD.find(name='div', attrs={'class', 'node-postdate'}).get_text()
        except:
            print bcolors.WARNING + 'The ' + str(iters) + 'th Page ' + str(i) + 'th date Error' + bcolors.ENDC
            date = ''
        data = (iters, title, link, date, keyword, content)
        self.insertData(data)

    def insertData(self, data):
        cursor = self.cnn.cursor()
        sql_insert = 'INSERT INTO StraitsTimesHistoryNews (page, title, link, postdate,keyword,content) VALUES (%s, %s, %s, %s,%s,%s)'
        try:
            cursor.execute(sql_insert, data)
        except mysql.connector.Error as e:
            print bcolors.WARNING + 'insert data error!{}'.format(e) + bcolors.ENDC
        finally:
            self.cnn.commit()
            cursor.close()

    def parseContentKeyword(self, newsurl):
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        html = requests.get(url=newsurl, headers=head)
        try:
            keyword = re.findall(r".*\"keyword\":\"(.*?)\",.*", html.text)
            soup = BeautifulSoup(html.text, 'lxml')
            matchContent = soup.find_all(name='p')
        except:
            print "Keyword or content match Error"
            return '', ''
        content = ''
        for i in range(len(matchContent) - 5):
            content += matchContent[i].get_text()
        return keyword[0], content

    def createTable(self):
        sqlCreateTable = "CREATE TABLE IF NOT EXISTS StraitsTimesHistoryNews (" \
                         "id       INT AUTO_INCREMENT PRIMARY KEY," \
                         "page     INT NOT NULL," \
                         "title    VARCHAR(1024) UNIQUE," \
                         "link     TEXT," \
                         "postdate TEXT," \
                         "keyword TEXT," \
                         "content TEXT)"
        cursor = self.cnn.cursor()
        try:
            cursor.execute(sqlCreateTable)
        except mysql.connector.Error as e:
            print bcolors.WARNING + 'create table StraitsTimesHistoryNews fails!{}'.format(e) + bcolors.ENDC
