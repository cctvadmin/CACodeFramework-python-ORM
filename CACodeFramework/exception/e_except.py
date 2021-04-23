from datetime import datetime
import warnings

from CACodeFramework.field import e_fields


def warn(obj, line, msg, f_warn, LogObject=None, task_name='\t\tMAIN'):
    """作者:CACode 最后编辑于2021/4/13

    输出日志并返回日志内容

    此方法不会中断程序运行

    格式：

        时间 类型 日志名称 对象地址 被调用行号 执行类型 信息
    示例：

        line:234: Warning: 2021-04-13 08:24:08.169 WARN CACode-Database-Operation [1907116304800] [line:234] [2021-04-13 08:24:08.169] 			:INITIALIZE THIS OBJECT
    """
    t = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    info = '{} {} {} [{}] [{}] [{}] \t\t\t:{}'.format(t, f_warn,
                                                      e_fields.LOG_OPERA_NAME,
                                                      id(obj),
                                                      obj.__str__(),
                                                      task_name,
                                                      msg)
    # 输出日志信息
    warnings.warn_explicit(info, category=Warning, filename='line', lineno=line)
    if LogObject is not None:
        LogObject.warn(info)
    return info


def error(cls, msg):
    """作者:CACode 最后编辑于2021/4/13

    抛出异常并终止程序执行
    Atte
    """
    raise cls(msg)
