import types


class AopModel_Object(object):
    """
        此类为AopModel提供所有操作
    """

    def __init__(self, before=None, after=None,
                 before_args=None, before_kwargs=None,
                 after_args=None, after_kwargs=None):
        # wraps(func)(self)
        # self.func = func
        # 初始化所有字段
        self.__before_func__ = before
        self.__before_args_data__ = before_args
        self.__before_kwargs_data__ = before_kwargs

        self.__after_func__ = after
        self.__after_args_data__ = after_args
        self.__after_kwargs_data__ = after_kwargs

    def set_func(self, func):
        self.func = func

    def set_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def start(self):
        """
        主操作
        """

        # self.func = args[0]
        self.init_fields()
        # wraps(self.func)(self)
        self.init_attr()

        # 解析参数需要
        # self.before_parse()
        # 执行before操作
        self.before_run()
        # 执行原始数据
        result = self.original_func()
        # after解析
        # self.after_parse(result)
        # after操作
        self.after_run(result)
        # 返回原始数据
        return result

    def init_fields(self):
        # 定义名称规则
        self.after = 'after'
        self.after_args = 'after_args'
        self.after_kwargs = 'after_kwargs'

        self.before = 'before'
        self.before_args = 'before_args'
        self.before_kwargs = 'before_kwargs'

        self.__after__ = '__after_func__'
        self.__after_args__ = '__after_args__'
        self.__after_kwargs__ = '__after_kwargs__'

        # 得到before参数的名称
        self.__before_name__ = self.format_name(self.before)
        self.__before_args_name__ = self.format_name(self.before_args)
        self.__before_kwargs_name__ = self.format_name(self.before_kwargs)

        # 得到after参数的名称

        self.__after_name__ = self.format_name(self.__after__)
        self.__after_args_name__ = self.format_name(self.__after_args__)
        self.__after_kwargs_name__ = self.format_name(self.__after_kwargs__)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def format_name(self, name):
        """
        格式化名称字符串
        """
        return '{}{}'.format(name, self.func.__name__)

    def setters(self, i1, i2, i3, k1, v1, k2, v2, k3, v3):
        """
        批量设置
        """
        if i1 in self.__dict__.keys():
            setattr(self, v1, self.__dict__[k1])
            if i2 in self.__dict__.keys():
                setattr(self, v2, self.__dict__[k2])
            if i3 in self.__dict__.keys():
                setattr(self, v3, self.__dict__[k3])

    def init_attr(self):
        """
        初始化cls下的字段
        通过使用setters下的setter()功能批量解析是否需要before或者after操作
        """

        self.setters(
            i1=self.before,
            i2=self.before_args,
            i3=self.before_kwargs,
            k1=self.before,
            k2=self.before_args,
            k3=self.before_kwargs,
            v3=self.__before_kwargs_name__,
            v1=self.__before_name__,
            v2=self.__before_args_name__,
        )

        self.setters(
            i1=self.after,
            i2=self.after_args,
            i3=self.after_kwargs,
            k1=self.after,
            k2=self.after_args,
            k3=self.after_kwargs,
            v1=self.__after_name__,
            v2=self.__after_args_name__,
            v3=self.__after_kwargs_name__
        )

    # def before_parse(self):
    #     """
    #     解析before参数的方法需要什么参数类型
    #     """
    #     __before_func__ = None
    #     __before_args_data__ = None
    #     __before_kwargs_data__ = None
    #     # 如果包含切入函数的字段
    #     if hasattr(self, self.__before_name__):
    #         # 得到参数的名称
    #         __before_func__ = getattr(self, self.__before_name__)
    #         if hasattr(self, self.__before_args_name__) and hasattr(self, self.__before_kwargs_name__):
    #
    #             __before_args_data__ = getattr(self, self.__before_args_name__)
    #             __before_kwargs_data__ = getattr(self, self.__before_kwargs_name__)
    #
    #         elif hasattr(self, self.__before_args_name__):
    #             __before_args_data__ = getattr(self, self.__before_args_name__)
    #
    #         elif hasattr(self, self.__before_kwargs_name__):
    #             __before_kwargs_data__ = getattr(self, self.__before_kwargs_name__)
    #
    #     # 批添加方法、参数和键值对
    #     self.__before_func__ = __before_func__
    #     self.__before_args_data__ = __before_args_data__
    #     self.__before_kwargs_data__ = __before_kwargs_data__

    def before_run(self):
        """
        执行before方法
        """
        if self.__before_func__ and self.__before_args_data__ and self.__before_kwargs_data__:
            self.__before_func__(*self.__before_args_data__, **self.__before_kwargs_data__)
        elif self.__before_func__ and self.__before_args_data__:
            self.__before_func__(*self.__before_args_data__)
        elif self.__before_func__ and self.__before_kwargs_data__:
            self.__before_func__(**self.__before_kwargs_data__)
        elif self.__before_func__:
            self.__before_func__()
        else:
            pass

    # def after_parse(self, result):
    #     """
    #     解析追加方法
    #     :param result:原始方法返回的值
    #     """
    #     __after_func__ = None
    #     __after_args_data__ = None
    #     __after_kwargs_data__ = {}
    #     # 如果包含切入函数的字段
    #     if hasattr(self, self.__after_name__):
    #         # 得到参数的名称
    #         __after_func__ = getattr(self, self.__after_name__)
    #         if hasattr(self, self.__after_args_name__) and hasattr(self, self.__after_kwargs_name__):
    #
    #             __after_args_data__ = getattr(self, self.__after_args_name__)
    #             __after_kwargs_data__ = getattr(self, self.__after_kwargs_name__)
    #
    #         elif hasattr(self, self.__after_args_name__):
    #             __after_args_data__ = getattr(self, self.__after_args_name__)
    #
    #         elif hasattr(self, self.__after_kwargs_name__):
    #             __after_kwargs_data__ = getattr(self, self.__after_kwargs_name__)
    #
    #     # 批添加方法、参数和键值对
    #     self.__after_func__ = __after_func__
    #     self.__after_args_data__ = __after_args_data__
    #     __after_kwargs_data__.update({'result': result})
    #     self.__after_kwargs_data__ = __after_kwargs_data__

    def after_run(self, result):
        """
        执行after方法
        """
        if self.__after_kwargs_data__ is None:
            self.__after_kwargs_data__ = {}

            self.__after_kwargs_data__.update({'result': result})
        if self.__after_func__ and self.__after_args_data__ and self.__after_kwargs_data__:
            self.__after_func__(*self.__after_args_data__, **self.__after_kwargs_data__)
        elif self.__after_func__ and self.__after_args_data__:
            self.__after_func__(*self.__after_args_data__)
        elif self.__after_func__ and self.__after_kwargs_data__:
            self.__after_func__(**self.__after_kwargs_data__)
        elif self.__after_func__:
            self.__after_func__()
        else:
            pass

    def original_func(self):
        """
        最后耍无赖方法返回函数执行的结果
        使用四个try逐一抛出
        """
        try:
            return self.func(*self.args, **self.kwargs)
        except TypeError as e:
            pass

        try:
            return self.func(*self.args)
        except TypeError as e:
            pass

        try:
            return self.func(**self.kwargs)
        except TypeError as e:
            pass

        try:
            return self.func()
        except TypeError as e:
            pass


def AopModel(before=None, after=None,
             before_args=None, before_kwargs=None,
             after_args=None, after_kwargs=None):
    """

        AOP切面模式：
            依赖AopModel装饰器,再在方法上加入@AopModel即可切入编程


        优点:

            当使用@AopModel时,内部函数将会逐级调用回调函数,执行循序是:
                - func(*self.args, **self.kwargs)
                - func(*self.args)
                - func(**self.kwargs)
                - func()
            这将意味着,如果你的参数传入错误时,AopModel依旧会遵循原始方法所使用的规则,最令人大跌眼镜的使用方法就是:
<code>
                def Before(**kwargs):
                    print('Before:', kwargs)
                # 此处的Before方法未存在args参数,而使用@AopModel时却传入了args
                @AopModel(before=Before,before_args=(0,1,2), before_kwargs={'1': '1'})
                def find_title_and_selects(self, **kwargs):

                    print('function task', kwargs['uid'])

                    _r = self.orm.find().where(index="<<100").end()

                    print(_r)

                    return _r
</code>
            其中包含参数有:
                before:切入时需要执行的函数

                before_args:切入的参数
                    传入的列表或元组类型数据
                    如果是需要使用当前pojo中的内容时，传参格式为:(pojo.字段名)
                    可扩展格式，例如需要传入字典

                before_kwargs:切入的参数 -- 传入的字典数据

                after:切出前需要执行的参数

                after_args:切出的参数
                    传入的列表或元组类型数据
                    如果是需要使用当前pojo中的内容时，传参格式为:('self.字段名')
                    可扩展格式，例如需要传入字典:('self.dict.key')

                after_kwargs:切出的参数 -- 传入的字典数据


        执行流程:

            Before->original->After

        Before注意事项:

            使用该参数时，方法具有返回值概不做处理,需要返回值内容可使用`global`定义一个全局字段用于保存数值

            当无法解析或者解析失败时m将使用pass关键字忽略操作

        After注意事项:

            使用该参数时，必须搭配至少一个result=None的kwargs存在于方法的形参中,

            当original方法执行完成将把返回值固定使用result键值对注入到该函数中

            当无法解析或者解析失败时m将使用pass关键字忽略操作



        Attributes:

             before:切入时需要执行的函数

             after:切出前需要执行的参数

             before_args:切入的参数
                传入的列表或元组类型数据
                如果是需要使用当前pojo中的内容时，传参格式为:(pojo.字段名)
                可扩展格式，例如需要传入字典

             before_kwargs:切入的参数 -- 传入的字典数据

             after_args:切出的参数
                传入的列表或元组类型数据
                如果是需要使用当前pojo中的内容时，传参格式为:('self.字段名')
                可扩展格式，例如需要传入字典:('self.dict.key')

             after_kwargs:切出的参数 -- 传入的字典数据


            """
    # 得到对象组
    aop_obj = AopModel_Object(before, after,
                              before_args, before_kwargs,
                              after_args, after_kwargs)

    def base_func(func):
        aop_obj.set_func(func)

        def _wrapper_(*args, **kwargs):
            aop_obj.set_args(*args, **kwargs)
            return aop_obj.start()

        return _wrapper_

    return base_func
