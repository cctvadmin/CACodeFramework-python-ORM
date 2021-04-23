import types
from functools import wraps


def Table(name, msg, **kwargs):
    """
    标注该类为一个表
    :param name:表的名称
    :param msg:表的描述
    :return:
    """

    def set_to_field(cls):
        setattr(cls, '__table_name__', name)
        setattr(cls, '__table_msg__', msg)
        for key, value in kwargs.items():
            setattr(cls, key, value)
        return cls

    return set_to_field


def Operations():
    """
    标注该类为一个操做
    :return:
    """

    def set_to_field(func):
        print('1111111')
        return func

    return set_to_field


def Select():
    def base_func(cls):
        cls_obj = cls()
        structured = cls_obj.__dict__
        args = []
        kwargs = {}
        if 'fields' in structured.keys():
            args.append(structured['fields'])

        for key, value in structured.items():
            if key is not 'fields':
                kwargs[key] = value

        def _wrapper_(*args, **kwargs):
            obj = cls_obj.meta()

            result = obj.orm.find(*args, **kwargs).end()

            return result

        return _wrapper_

    return base_func
