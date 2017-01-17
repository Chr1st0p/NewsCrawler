from time import clock

from todayOnlineHistoryNews import todayNews
from straitstimesHistoryNews import straitsTimesNews
from getNewsDemo import getContentKeyword
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

if __name__ == '__main__':
    n1 = straitsTimesNews()
    start = clock()
    n1.start()
    end = clock()
    print (end - start)
