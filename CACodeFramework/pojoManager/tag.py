from CACodeFramework.util import JsonUtil

"""
这个文件用来为pojo对象做标记，当对象为空或为以下任意类型时
insert操做将会忽略该字段，find操作不会处理为空的字段
"""


class baseTag(object):
    def __init__(self,
                 table_name=None,
                 name=None,
                 length=None,
                 d_point=None,
                 t_type='varchar',
                 is_null=False,
                 primary_key=False,
                 comment="",
                 auto_field=False,
                 auto_time=False,
                 update_auto_time=False):
        """
        :param table_name:表名称
        :param name:字段名
        :param length:长度
        :param d_point:小数点
        :param t_type:类型
        :param is_null:允许为空
        :param primary_key:键
        :param comment:注释
        :param auto_field:自增长键
        :param auto_time:默认设置当前时间
        :param update_auto_time:默认设置当前时间并根据当前时间更新
        """
        self.update_auto_time = update_auto_time
        self.auto_time = auto_time
        self.autoField = auto_field
        self.table_name = table_name
        self.comment = comment
        self.primary_key = primary_key
        self.is_null = is_null
        self.d_point = d_point
        self.name = name
        self.t_type = t_type
        self.length = length
        # 如果使用的是被继承的子类，那么在这里就会有一个名为fields的字段
        # 将所有自定义字段
        if self.fields:
            for key, value in self.fields.items():
                setattr(self, key, value)

            del self.fields

    def get_field(self, name):
        """
        获得字段
        """
        return getattr(self, name)

    def set_field(self, name, value):
        """
        设置值
        """
        setattr(self, name, value)

    def get_table(self, bf):
        """
        获取表数据结构
        """
        if bf:
            return JsonUtil.parse(self, bf)
        return JsonUtil.load(JsonUtil.parse(self))


class tinyintField(baseTag):

    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(tinyintField, self).__init__(**kwargs)


class intField(baseTag):
    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(intField, self).__init__(**kwargs)


class bigintField(baseTag):
    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(bigintField, self).__init__(**kwargs)


class floatField(baseTag):
    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(floatField, self).__init__(**kwargs)


class doubleField(baseTag):
    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(doubleField, self).__init__(**kwargs)


class datetimeField(baseTag):
    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(datetimeField, self).__init__(**kwargs)


class charField(baseTag):
    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(charField, self).__init__(**kwargs)


class varcharField(baseTag):
    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(varcharField, self).__init__(**kwargs)


class textField(baseTag):
    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(textField, self).__init__(**kwargs)


class tinytextField(baseTag):
    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(tinytextField, self).__init__(**kwargs)


class longtextField(baseTag):
    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(longtextField, self).__init__(**kwargs)


def update_field(**kwargs):
    """
    更新字典配置
    """

    def no_rep(key, value, **kwargs):
        """
        不存在则替换
        """
        if key not in kwargs.keys():
            kwargs[key] = value
        return kwargs

    def has_attr(key, **kwargs):
        if key in kwargs:
            return kwargs[key]
        return None

    kwargs.update(no_rep('table_name', has_attr('__table_name__', **kwargs), **kwargs))
    kwargs.update(no_rep('name', has_attr('name', **kwargs), **kwargs))
    kwargs.update(no_rep('length', has_attr('length', **kwargs), **kwargs))
    kwargs.update(no_rep('d_point', has_attr('d_point', **kwargs), **kwargs))
    kwargs.update(no_rep('t_type', has_attr('t_type', **kwargs), **kwargs))
    kwargs.update(no_rep('is_null', has_attr('is_null', **kwargs), **kwargs))
    kwargs.update(no_rep('primary_key', has_attr('primary_key', **kwargs), **kwargs))
    kwargs.update(no_rep('comment', has_attr('comment', **kwargs), **kwargs))
    kwargs.update(no_rep('auto_field', has_attr('auto_field', **kwargs), **kwargs))
    kwargs.update(no_rep('auto_time', has_attr('auto_time', **kwargs), **kwargs))
    kwargs.update(no_rep('update_auto_time', has_attr('update_auto_time', **kwargs), **kwargs))
    return kwargs
