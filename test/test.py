import threading
import uuid

from CACodeFramework.anno.annos import Table, Select
from CACodeFramework.anno.aop import AopModel
from CACodeFramework.pojoManager import PojoManager

from CACodeFramework.util import Config, JsonUtil


class ConF(Config.config):
    def __init__(self,
                 host='localhost',
                 port=3306,
                 database='demo',
                 user='root',
                 password='123456',
                 charset='utf8'):
        conf = {
            "print_sql": True,
            "last_id": True,
        }

        super(ConF, self).__init__(host, port, database, user, password, charset, conf=conf)


def Before(**kwargs):
    print('Before:', kwargs)


def After(*args, **kwargs):
    print('After', args)
    print('Result:', kwargs)


@Table(name="demo_table", msg="demo message")
class Demo(PojoManager.pojo):
    def __init__(self, **kwargs):
        self.index = PojoManager.tag.intField(name='index', primary_key=True)
        self.title = PojoManager.tag.varcharField(length=255)
        self.selects = PojoManager.tag.varcharField(length=255)
        self.success = PojoManager.tag.varcharField(length=255)
        super(Demo, self).__init__(config_obj=ConF(), close_log=True, **kwargs)

    @AopModel(before=Before,
              before_kwargs={'1': '1'},
              after=After)
    def find_title_and_selects(self, **kwargs):
        print('function task', kwargs['uid'])
        _r = self.orm.find().where(index="<<100").end()
        print(_r)
        return _r

    @Select()
    class find_test(PojoManager.Operation):
        def __int__(self):
            self.fields = [
                'all'
            ]

        def meta(self):
            return Demo()


d = Demo()


def setData():
    a = []
    h = Demo()
    for i in range(2):
        h = Demo(title="test title", selects="test selects", success='false')
        a.append(h)
        # _result = testClass.insert_one(pojo=h)
        _r = Demo().orm.insert(h).end()
    # h.insert_many(pojo_list=a)
    # _result = testClass.insert_many(pojo_list=pojos)
    # print('受影响行数：{}\t,\t已插入：{}'.format(_result, i))


data_count = 0


def th():
    def A():
        for i in range(100):
            d = Demo()
            a = d.find_sql(sql='SELECT * FROM demo_table')
            global data_count
            data_count += len(a)

    def B():
        for i in range(100):
            b = Demo().find_many(sql='SELECT * FROM demo_table')
            global data_count
            data_count += len(b)

    def C():
        for i in range(100):
            c = Demo().find_all()
            global data_count
            data_count += len(c)

    def D():
        for i in range(100):
            d = Demo().find_by_field('title', 'selects')
            global data_count
            data_count += len(d)

    _a = threading.Thread(target=A)
    _b = threading.Thread(target=B)
    _c = threading.Thread(target=C)
    _d = threading.Thread(target=D)
    return _a, _b, _c, _d


if __name__ == '__main__':
    # setData()
    # c = Demo().orm.find('count(*)', asses=['c'], h_func=True).end()[0]
    # print('count:', c.c)
    # t1 = time.time()
    # t = th()
    # for i in t:
    #     i.start()
    #     i.join()
    # t2 = time.time()
    # print('time:', t2 - t1)
    # print('data count:', data_count)
    # print('average:', data_count / (t2 - t1))
    d = Demo()
    u = uuid.uuid1()
    # result = d.find_title_and_selects(uid=u)
    # print(JsonUtil.parse(d, True))
    a = d.find_test().run()
    # d.before_find_title_and_selects(*d.before_args_find_title_and_selects,
    #                                 **d.before_kwargs_find_title_and_selects)
    # _r = d.orm.update().set(success='true').where(index=17034).end()
    # print(_r)
