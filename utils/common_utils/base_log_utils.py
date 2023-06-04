import logging
import os
from logging.handlers import TimedRotatingFileHandler

from colorlog import ColoredFormatter
import platform


class BaseLoggerFactory():

    @classmethod
    def create_dir(cls, path):
        """
        目录不存在就创建
        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)

    """
    %(asctime)s 字符串形式的当前时间。默认格式是“2021-09-08 16:49:45,896”。逗号后面的是毫秒
    %(created)f 时间戳, 等同于time.time()
    %(relativeCreated)d 日志发生的时间相对于logging模块加载时间的相对毫秒数
    %(msecs)d 日志时间发生的毫秒部分
    %(levelname)s 日志级别str格式
    %(levelno)s 日志级别数字形式(10, 20, 30, 40, 50)
    %(name)s 日志器名称, 默认root
    %(message)s 日志内容
    %(pathname)s 日志全路径
    %(filename)s 文件名含后缀
    %(module)s 文件名不含后缀
    %(lineno)d 调用日志记录函数源代码的行号
    %(funcName)s 调用日志记录函数的函数名
    %(process)d 进程id
    %(processName)s 进程名称
    %(thread)d 线程ID
    %(threadName)s 线程名称
    """
    log_format = '%(asctime)s [%(levelname)s] -%(threadName)s- - %(name)s - %(message)s'
    log_level = logging.INFO
    log_file = 'data.log'
    log_name = 'data'
    log_dir = 'c:\logs' if 'Windows' == platform.system() else '/usr/local/logs'

    @classmethod
    def getLogger(cls, log_dir=None, log_name=None, log_file=None, log_format=None, log_level=None):
        cls.log_dir = log_dir if log_dir else cls.log_dir
        cls.create_dir(cls.log_dir)
        # 默认的控制台输出
        fmt = ColoredFormatter(
            # log_color设置颜色，如果使用reset，则后续颜色不改变，可使用第八行配置运行下看下效果
            "%(log_color)s" + cls.log_format,
            # "%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s",
            datefmt=None,
            reset=True,
            # 设置不同等级颜色
            log_colors={
                'DEBUG': 'fg_thin_cyan',
                'INFO': 'thin_green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            },
            secondary_log_colors={},
            style='%'
        )
        console = logging.StreamHandler()
        console.setFormatter(fmt)

        cls.log_format = log_format if log_format else cls.log_format
        cls.log_level = log_level if log_level else cls.log_level
        cls.log_file = log_file if log_file else cls.log_file
        cls.log_name = log_name if log_name else cls.log_name
        log = logging.getLogger(cls.log_name)
        fmt = logging.Formatter(cls.log_format)
        log_handel = TimedRotatingFileHandler(cls.log_dir + os.sep + cls.log_file, when='D', interval=1, backupCount=30)
        log_handel.suffix = "%Y-%m-%d.log"
        # log_handel = logging.FileHandler(cls.log_file)
        log_handel.setFormatter(fmt)
        log.setLevel(cls.log_level)
        log.addHandler(log_handel)
        log.addHandler(console)
        return log


if __name__ == '__main__':
    log = BaseLoggerFactory.getLogger()
    log.info('info')
    log.debug('debug')
    log.error('error')
    log.warning('warning')
    log.critical('critical')
