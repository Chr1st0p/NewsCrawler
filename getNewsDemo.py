import requests
from bs4 import BeautifulSoup
import re


def getNewsHtml(targetUrl):
    # header;
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    print 'Start Get News:'
    html = requests.get(targetUrl, headers=head)
    soup = BeautifulSoup(html.text, 'lxml')

    # delete the div with class=panel-panel right,
    # without this step, the result in next step will be class=panel-panel right + class=right;
    for div in soup.find_all("div", {'class': 'panel-panel right'}):
        div.decompose()

    # match the news div,the first one is the brief news which is useless,only 2-10 are the news;
    matchContent = soup.find_all(name='div', attrs={'class', 'right'})

    # separete the title, link, date, abstract;
    for i in range(1, 10):
        try:
            paraseNews(matchContent[i])
        except:
            print str(i) + 'Error'


def paraseNews(news):
    print news.find(name='h2', attrs={'class', 'node__title node-title'}).get_text()
    print news.find(name='h2').find(name='a').get('href')
    print news.find(name='div', attrs={'class', 'timeago-highlight'}).get_text()
    print news.find(name='p').get_text()


def getContentKeyword(newsurl):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    html = requests.get(url=newsurl, headers=head)
    print re.findall(r".*\"keyword\":\"(.*?)\",.*", html.text)
    soup = BeautifulSoup(html.text, 'lxml')
    content = soup.find_all(name='p')
    for i in range(len(content) - 4):
        print content[i].get_text()


if __name__ == '__main__':
    getNewsHtml('http://www.todayonline.com/singapore?page=5')
