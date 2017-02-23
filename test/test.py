from src import TodayOnlineHistoryNews as toNews

if __name__ == '__main__':
    n1 = toNews.TodayNews()
    toNews.getHtml(2356)
    print "Done"
