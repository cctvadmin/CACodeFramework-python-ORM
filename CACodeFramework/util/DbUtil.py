import sys

from CACodeFramework.util.Log import CACodeLog
from dbutils.pooled_db import PooledDB
import pymysql

from CACodeFramework.exception import e_except
from CACodeFramework.field import e_fields


def parse_kwa(db, **kwargs):
    """
    解析并执行sql

    :param db:db_util对象
    :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
    """
    try:
        cursor = db.cursor()
        if 'params' in kwargs.keys():
            sql = cursor.mogrify(kwargs['sql'], kwargs['params'])
        else:
            sql = kwargs['sql']
        if 'print_sql' in kwargs.keys() and kwargs['print_sql'] is True:
            _l = sys._getframe().f_back.f_lineno
            e_except.warn(obj=db, line=_l, task_name='Print Sql', f_warn=e_fields.INFO, msg=sql)
            CACodeLog.log(_obj=db, msg='Being Initialize this object')
        cursor.execute(sql)
        return cursor
    except Exception as e:
        db.rollback()
        raise e


class Db_opera(object):
    """
    操作数据库类
    """

    def __init__(self, host, port, user, password, database, charset, creator=pymysql, maxconnections=6, mincached=2,
                 maxcached=5, maxshared=3, blocking=True, setsession=[], ping=0, POOL=None):
        """
        初始化配置
        以下参数与PooledDB一致
        :param creator:默认即可
        :param maxconnections:默认即可
        :param mincached:默认即可
        :param maxcached:默认即可
        :param maxshared:默认即可
        :param blocking:默认即可
        :param setsession:默认即可
        :param ping:默认即可
        :param host:数据库IP地址
        :param port:端口
        :param user:用户名,如root
        :param password:密码
        :param database:数据库名
        :param charset:编码格式
        :param POOL:使用自定义的PooledDB,不建议
        """
        self.creator = creator
        self.maxconnections = maxconnections
        self.mincached = mincached
        self.maxcached = maxcached
        self.maxshared = maxshared
        self.blocking = blocking
        self.setsession = setsession
        self.ping = ping
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.POOL = POOL
        self.init_config()

    def init_config(self):
        """
        初始化数据库连接池
        """
        if self.POOL is None:
            self.POOL = PooledDB(creator=self.creator, maxconnections=self.maxconnections, mincached=self.mincached,
                                 maxcached=self.maxcached,
                                 maxshared=self.maxshared,
                                 blocking=self.blocking,
                                 setsession=self.setsession,
                                 ping=0, host=self.host, port=self.port,
                                 user=self.user,
                                 password=self.password, database=self.database, charset=self.charset)

    def get_conn(self):
        """
        获取数据库连接池
        :return:
        """
        return self.POOL.connection()

    def select(self, **kwargs):
        """
        查找多个
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
        :return:
        """
        db = self.get_conn()
        try:
            cursor = parse_kwa(db=db, **kwargs)
            # 列名
            col = cursor.description
            data = []
            while True:
                one = cursor.fetchone()
                if one is None:
                    break
                else:
                    data.append(one)
            db.close()
            _result = []
            for data_index, data_value in enumerate(data):
                _messy = {}
                for item_index, item_value in enumerate(data_value):
                    _messy[col[item_index][0]] = item_value
                _result.append(_messy)
            return _result
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def insert(self, **kwargs):
        """
        执行插入语句
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        """
        db = self.get_conn()
        try:
            cursor = parse_kwa(db=db, **kwargs)
            db.commit()
            # 最后一行ID
            last = cursor.lastrowid
            # 受影响行数
            rowcount = cursor.rowcount
            # 返回受影响行数
            if kwargs['last_id']:
                return rowcount, last
            else:
                return rowcount
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def update(self, **kwargs):
        """
        执行更新语句
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        """
        return self.insert(**kwargs)

    def delete(self, **kwargs):
        """
        执行删除语句
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        """
        self.insert(**kwargs)
