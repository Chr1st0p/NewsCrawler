class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class DbConfig:
    newsDataConfig = {'host': '127.0.0.1',
                      'user': 'root',
                      'password': 'qwerty123456',
                      'port': 3306,
                      'database': 'newsdata',
                      'charset': 'utf8'
                      }