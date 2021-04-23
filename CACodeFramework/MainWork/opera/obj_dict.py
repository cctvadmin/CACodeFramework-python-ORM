import copy
import sys

from CACodeFramework.exception import e_except
from CACodeFramework.field import e_fields
from CACodeFramework.util.ParseUtil import ParseUtil


class parses(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def log(self, _obj, msg, name='\t\tTask', LogObject=None):
        """
        输出任务执行日志

        :param _obj:任务对象的值

        """
        # 获得该函数被调用前的行号
        _l = sys._getframe().f_back.f_lineno
        # 格式：时间 类型 日志名称 对象地址 被调用行号 执行类型 信息
        info = e_except.warn(obj=_obj, line=_l, task_name=name, f_warn=e_fields.INFO, msg=msg, LogObject=LogObject)

    def last_id(self, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        遵循规则：

            内部>配置文件

        是否包含返回最后一行ID的配置

        只存在于更新操做的方法内，如：

            insert,

            update,

            delete

         Attributes:

             conf_obj:配置类
        """
        conf_obj = kwargs['config_obj']
        if 'last_id' not in kwargs.keys():
            if 'last_id' in conf_obj.conf.keys():
                kwargs['last_id'] = conf_obj.conf['last_id']
            else:
                kwargs['last_id'] = False
        return kwargs

    def print_sql(self, **kwargs):
        """
        遵循规则：
            内部>配置文件

        是否包含打印sql的配置

        存在于所有数据库操做

        Attributes:
             conf_obj:配置类
        """
        conf_obj = kwargs['config_obj']
        if 'print_sql' not in kwargs.keys():
            if 'print_sql' in conf_obj.conf.keys():
                kwargs['print_sql'] = conf_obj.conf['print_sql']
            else:
                kwargs['print_sql'] = False
        return kwargs

    def parse_insert(self, pojo, __table_name__):
        """
        解析插入语句

        INSERT INTO `__table_name__`(`title`,'selects') VALUE ('','')

        :param pojo:POJO对象
        :param __table_name__:表名
        :return:
        """
        _dict = pojo.to_dict()
        # 得到所有的键
        keys = pojo.fields
        # 在得到值之后解析是否为空并删除为空的值和对应的字段
        cp_value = []
        values = [getattr(pojo, v) for v in keys]
        for i, j in enumerate(values):
            if j is None or pojo.eq_default(j):
                del keys[i]
            else:
                cp_value.append(j)
        return ParseUtil().parse_insert(keys, cp_value, __table_name__)

    def parse_obj(self, data: dict, participants):
        """
        将数据解析成对象
        注意事项:
            数据来源必须是DbUtil下查询出来的
        :param data:单行数据
        :param participants:参与解析的对象
        :return:POJO对象
        """
        # 深度复制对象
        part_obj = copy.copy(participants)
        for key, value in data.items():
            setattr(part_obj, key, value)
        return part_obj
