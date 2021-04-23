from CACodeFramework.MainWork.CACodePureORM import CACodePureORM
from CACodeFramework.pojoManager import tag
from CACodeFramework.util import JsonUtil
from CACodeFramework.MainWork import CACodeRepository
from abc import ABCMeta, abstractmethod


class pojo(CACodeRepository.Repository):
    def __init__(self, config_obj=None, log_conf=None, close_log=False, **kwargs):
        """
        初始化ORM框架
        """
        self.__table_name__ = self.__table_name__
        self.__table_msg__ = self.__table_msg__
        self.fields = self.init_fields()
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        super(pojo, self).__init__(config_obj=config_obj,
                                   participants=self,
                                   log_conf=log_conf,
                                   close_log=close_log)

    def init_fields(self):
        """
        初始化字段
        """
        fields = self.__dict__
        fds = {}
        for key, value in fields.items():
            # 取出这个值引用对象的父类
            try:
                t_v = value.__class__.__bases__
                t_bf = tag.baseTag
                if t_v[0] == t_bf:
                    fds[key] = value
            except SyntaxError:
                continue
        return fds

    def to_json(self):
        """
        将此对象转换为json

        无视时间报错
        """
        return JsonUtil.parse(self)

    def to_dict(self):
        """
        将此对象转换成字典格式
        """
        return self.fields

    def eq_default(self, val):
        """
        是否等于默认值
        """
        try:
            t_v = val.__class__.__bases__
            t_bf = tag.baseTag
            return t_v[len(t_v) - 1] == t_bf
        except SyntaxError:
            return False

    @property
    def orm(self):
        """
        转ORM框架
        """
        return CACodePureORM(self)


class Operation(metaclass=ABCMeta):
    def __int__(self):
        pass

    @abstractmethod
    def meta(self):
        pass

    def run(self):
        self.run_operation()
