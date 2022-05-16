import datetime
import sys

class LogBase():

    __version__ = '1.0'

    def __gettime():
        now_time = datetime.datetime.now()
        return datetime.datetime.strftime(now_time,'%Y-%m-%d %H:%M:%S')

    def log(self, txt, dt=None):
        ''' 提供记录功能 '''
        dt = dt or LogBase.__gettime()

        f_code = sys._getframe().f_back.f_code
        f_back = sys._getframe().f_back

        print('%s %s.%s.%d : %s' % (dt, f_code.co_filename, f_code.co_name, f_back.f_lineno , txt))


# if __name__ == '__main__':
#     print(LogBase.__name__ + ' version:' + LogBase.__version__)