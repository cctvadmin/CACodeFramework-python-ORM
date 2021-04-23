# 适用于 Python 语言所有web架构 的 ORM( Object-Relational-Mapping ) 框架

# 安装

    pip命令：pip install CACodeFramework

# 作者

    author:cacode  
    
    email:cacode@163.com
    
    皮皮虾：你在写臭虫?
    
    西瓜视频：你在写臭虫?
    
    bilibili：你在写臭虫?
    
    抖音：你在写臭虫?
    
    gitee：ca_code
    
    github:cctvadmin
    
    视频教程：先等我缓几天，一个人真的忙不过来

# 招募开发者共同维护此项目

要求熟悉 `python` 语言,熟悉 `native` , `cpython`

或

熟悉 `java` ,精通 `JPA` , `Hibernate` ,精通`sprint`底层`ICO`容器

并且

熟悉所有设计模式，精通多线程、多进程处理

一定

热爱开源！！！！！

另外

需要一个写文档的、录教程的

联系

简历发送至邮箱cacode@163.com，标题 CACodeFramework-姓名-语言

# 逻辑处理流程图

![流程图](./imgs/lct.png "流程图")

# 版本更新:

## 1.1.2.1

- 修复多线程下查询报错
- 查询速度显著提高
- 使用ThreadLocal保持线程单一性
- 去除彩蛋
    - 框架就应该有框架的样子

- 教程正在录制中。。。

## 1.1.1.1

-- 修复半自动Repository的insert相关解析失败  
-- 修复全自动ORM执行失败  
-- 新增group_by(*args)  
-- 新增一个2048小彩蛋

## 1.1.0.03:

- 修复JsonUtil.parse(obj)
    - 部分字典dict解析失败

- 新增asses字段
    - 可以使用：orm.find('title', 'success', asses=['t', None]).end()将索引对应字段转成另一个别名 最后的结果就是：SELECT `title` FROM `demo_table`
      as t

## 1.1.0.2:

- 修复find
    - 无法返回POJO
    - 解析深度不够

- 修复PureORM
    - 修复返回值为dict而非POJO问题

## 1.0.2.1:

- 修复JsonUtil
    - 无法解析对象
    - 解析不完整
    - 解析不到深层

- 新增纯ORM模式
    - 增加类PureORM(object)
        - __init__(repository)
        - insert()
        - delete()
        - update()
        - by(*args)
        - order_by(*args)
        - desc()
        - set(**kwargs)
        - where(**kwargs)
        - limit(star,end)
        - ander(**kwargs)
        - run()
        - end()

# 使用指北:

内部配置规则：

    内部参数 大于 配置文件
    你可以像理解css一样理解

## 基本代码 base code

我怕有人因为没看说明调用报错找不到原因  
按照这个demo可以运行你的第一份使用CACodeFramework的代码  
前提是你已经认真看完教程

以下内容均依赖这个代码

    from CACodeFramework.MainWork import CACodeRepository, CACodePojo
    from CACodeFramework.MainWork.Annotations import Table
    from CACodeFramework.MainWork.CACodePureORM import CACodePureORM
    from CACodeFramework.util import Config, JsonUtil
    
    
    class ConF(Config.config):
        def __init__(self, host='localhost', port=3306, database='demo', user='root', password='123456', charset='utf8'):
            conf = {
                "print_sql": True,
                "last_id": True,
            }
            super(ConF, self).__init__(host, port, database, user, password, charset, conf=conf)
    
    
    class Demo(CACodePojo.POJO):
        def __init__(self):
            self.index = None
            self.title = None
            self.selects = None
            self.success = None
    
    
    @Table(name="demo_table", msg="demo message")
    class TestClass(CACodeRepository.Repository):
        def __init__(self):
            super(TestClass, self).__init__(config_obj=ConF(), participants=Demo())
    
    
    testClass = TestClass()
    orm = CACodePureORM(testClass)

## 基本语法符号

在这个框架中  
大于号： `>>`  
小于号：`<<`  
只有这两个符号才是做重复处理，其他的照常编写

## 工具类

### JsonUtil

#### JsonUtil.parse(obj) -> dict:

    将dict解析成json

#### JsonUtil.load(obj) -> dict:

    将json解析成dict

------

## 半自动:

### 增

#### insert_sql(**kwargs)->(tuple(int,int)):

    使用sql插入
    :param kwargs:包含所有参数:
            pojo:参照对象
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
    :return rowcount,last_id if last_id=True

教程编写匆忙，如果错误请务必联系我们

##### 示例

    _result = testClass.insert_sql(
        sql="INSERT INTO `demo_table` (`title`,`selects`,`success`) VALUES (%s,%s,%s)",
        params=['test title', 'test selects', 'false'])
    print(_result)

##### 返回结果

    INSERT INTO `demo_table` (`title`,`selects`,`success`) VALUES ('test title','test selects','false')
    (1, 5)

##### 示例解释

调用 `insert_sql()` 方法，并设置使用 `%s` 加以处理的sql语句

------

#### insert_one(**kwargs)->(tuple(int,int)):

    插入属性:
        返回受影响行数
    :param kwargs:包含所有参数:
        pojo:参照对象
        last_id:是否需要返回最后一行数据,默认False
        params:需要填充的字段
    :return:rowcount,last_id if last_id=True

教程编写匆忙，如果错误请务必联系我们

##### 示例

    h = Demo()
    h.title = "test title"
    h.selects = "test selects"
    h.success = "false"
    _result = testClass.insert_one(pojo=h)
    print(_result)

##### 返回结果

    INSERT INTO `demo_table` (`title`,`selects`,`success`) VALUES ('test title','test selects','false')
    (1, 6)

##### 示例解释

调用 `insert_one()` 方法，并设置pojo为一个实体类对象，框架内部会自动转换为合适的参数构造并执行  
最后返回受影响行数和最后一行数据的ID
------

#### insert_many(**kwargs)->(tuple(int,int)):

    插入多行
        这个是用insert_one插入多行
    :param kwargs:包含所有参数:
        pojo_list:参照对象列表
        last_id:是否需要返回最后一行数据,默认False
        sql:处理过并加上%s的sql语句
        params:需要填充的字段
    :return:list[rowcount,last_id if last_id=True]

教程编写匆忙，如果错误请务必联系我们

##### 示例

    pojos = []
    for i in range(2):
        h = Demo()
        h.title = "test title"
        h.selects = "test selects"
        h.success = "false"
        pojos.append(h)
    _result = testClass.insert_many(pojo_list=pojos)
    print(_result)

##### 返回结果

     INSERT INTO `demo_table` (`title`,`selects`,`success`) VALUES ('test title','test selects','false')
     INSERT INTO `demo_table` (`title`,`selects`,`success`) VALUES ('test title','test selects','false')
    [(1, 10), (1, 11)]

##### 示例解释

调用 `insert_many()` 方法，并设置pojo_list为一个多个实体类对象的集合，内部会自动将其分解为多个个体执行  
最后返回受影响行数和最后一行数据的ID

### 删

#### update(sql):

    由于删除也是更新操做，所以在CACodeFramework种，delete操做等同于update操做
    故不设置delete

### 改

#### update(**kwargs):

##### 示例

    _result = testClass.update(sql='update `demo_table` set title=%s where `index` < %s', params=['test update', 7])
    print(_result)

##### 返回结果

    update `demo_table` set title='test update' where `index` < 7
    (6, 0)

##### 示例解释

调用 `update()` 方法，并设置更新语句  
最后返回受影响行数 无法返回最后一行ID

### 查

#### find_sql(**kwargs):

    返回多个数据并用list包装:
        - 可自动化操作
        - 请尽量使用find_many(sql)操作
    :param kwargs:包含所有参数:
        pojo:参照对象
        last_id:是否需要返回最后一行数据,默认False
        sql:处理过并加上%s的sql语句
        params:需要填充的字段
        print_sql:是否打印sql语句

##### 示例

    _result = testClass.find_sql(sql='SELECT * FROM demo_table WHERE `index`=%s', params=[3])
    print(_result)

##### 返回结果

    SELECT * FROM demo_table WHERE `index`=3
    [{'index': 3, 'title': 'test update', 'selects': '60', 'success': 'true'}]

##### 示例解释

调用 `find_sql()` 方法，并设置查询sql语句 内部将结果封装成list返回

#### find_all(**kwargs):

    查询所有
    :return:将所有数据封装成POJO对象并返回

##### 示例

    _result = testClass.find_all()
    print(_result)

##### 返回结果

     SELECT `index`,`title`,`selects`,`success` FROM demo_table
    [<__main__.Demo object at 0x00000214D61DB8E0>,
    <__main__.Demo object at 0x00000214D61DBA60>,
    <__main__.Demo object at 0x00000214D61DBA90>,
    ....]

##### 示例解释

调用 `find_all()` 方法，将所有数据封装成POJO对象返回，其返回的item内部构造类似：

    'pojo':{'index': 1, 'title': 'test update', 'selects': '60', 'success': 'false'}

#### find_by_field(**kwargs):

    只查询指定名称的字段,如:
        SELECT user_name FROM `user`
        即可参与仅解析user_name为主的POJO对象
    :param args:需要参与解析的字段名
    :return:将所有数据封装成POJO对象并返回

##### 示例

    _result = testClass.find_by_field('title', 'selects')
    print(_result)

##### 返回结果

    SELECT `title`,`selects` FROM demo_table
    [<__main__.Demo object at 0x000002997F2D1A30>,
    <__main__.Demo object at 0x000002997F2D1BE0,
    ....>,

##### 示例解释

调用 `find_by_field()` 方法，查询所有保留的字段，其返回的item内部构造类似：

    'pojo':{'index': None, 'title': 'test update', 'selects': '60', 'success': None}

#### find_one(**kwargs):

    查找第一条数据
        可以是一条
        也可以是很多条中的第一条
    code:
        _result = self.find_many(**kwargs)
        if len(_result) == 0:
            return None
        else:
            return _result[0]
    :param kwargs:包含所有参数:
        pojo:参照对象
        last_id:是否需要返回最后一行数据,默认False
        sql:处理过并加上%s的sql语句
        params:需要填充的字段
        print_sql:是否打印sql语句
    :return 返回使用find_many()的结果种第一条

##### 示例

    _result = testClass.find_one(sql='select * from `demo_table` where `index`=%s', params=[3])
    print(_result)

##### 返回结果

    select * from `demo_table` where `index`=3
    <__main__.Demo object at 0x000001B30AF71B50>

##### 示例解释

    调用 `find_one()` 方法，查询所有保留的字段，其返回值内部构造类似：
    'pojo':{'index': None, 'title': 'test update', 'selects': '60', 'success': None}

#### find_many(sql):

##### 示例

    _result = testClass.find_many(sql='select * from `demo_table` where `index`<%s', params=[3])
    print(_result)

##### 返回结果

    select * from `demo_table` where `index`<3
    [<__main__.Demo object at 0x000002096712AA60>, <__main__.Demo object at 0x000002096712AAC0>]

##### 示例解释

参考 `find_by_field()` ，因为该方法将POJO类的字段作为`find_by_field()`的参数并执行

------

## 全自动:

### 增

#### insert(pojo):

    插入一条数据
    example:
        insert()
        insert('c1','c2')
    :param pojo:需要插入的对象

##### 示例

    h = Demo()
    h.title = "test title"
    h.selects = "test selects"
    h.success = "false"
    _result = orm.insert(h).end()
    print(_result)

##### 返回结果

     INSERT INTO `demo_table` ( `title`,`selects`,`success` ) VALUES  ( 'test title','test selects','false' )
    (1, 18)

##### 示例解释

调用 `insert()`方法并传入一个POJO对象，实现对该表的插入，并按照配置返回受影响行数和最后一行的ID

### 删

#### delete():

##### 示例

    _orm = orm.delete().where(index='<<3').end()
    print(_orm)

##### 返回结果

     DELETE  FROM `demo_table` WHERE `index`<<'3'
    (3, 0)

##### 示例解释

调用 `delete()`方法并设置where内的参数即可删除数据，请一定要设置where，否则将像sql语句那样执行全部删除

### 改

#### update(sql):

    更新
    example:
        update().set(key=value).where(key1=value1)

##### 示例

    _orm = orm.update().set(title='test', selects='selects').where(index='<<3').end()
    print(_orm)

##### 返回结果

    UPDATE `demo_table` SET `title`='test',`selects`='selects' WHERE `index`<'3'
    (2, 0)

##### 示例解释

调用 `update()`方法并设置`set()`内参数和`where()`内参数即可更改该行数据，返回受影响行数，没有last_id是因为不支持

### 查

#### find(*args):

##### 示例

    _orm = orm.find('All').end()
    print(_orm)

    _orm = orm.find('title','selects').where(index='>>3').end()
    print(_orm)

##### 返回结果

     SELECT `index`,`title`,`selects`,`success` FROM `demo_table`
    [{'index': 1, 'title': 'test', 'selects': 'selects', 'success': 'false'},
    {'index': 2, 'title': 'test', 'selects': 'selects', 'success': 'false'},
    ....]
    SELECT `title`,`selects` FROM `demo_table` WHERE `index`>'3'
    [{'title': '100', 'selects': 'selects'}, 
    {'title': '100', 'selects': 'selects'}, 
    ....]

##### 示例解释

调用`find()`方法传入`all`关键字为查询所有数据  
调用`find()`方法传入字段名为查询指定字段的所有数据  
调用`find().where()`方法传入字段名为查询指定字段并且满足条件的所有数据

### 复杂

#### order_by(**args):

#### desc():

#### limit(star=0,end=None):

#### order_by(**args):

#### 以上复杂方法使用同一案例解释:

##### 示例代码

    多条
    _orm = orm.find('title', 'selects').where(index='>>1').order_by('index', 'title').desc().limit(star=0, end=3).end()
    print(_orm)
    单条
    _orm = orm.find('title', 'selects').where(index='>>1').order_by('index', 'title').desc().limit(star=1).end()
    print(_orm)

##### 返回结果

    结果1
     SELECT `title`,`selects` FROM `demo_table` WHERE `index`>'1' ORDER BY `index` AND `title`  DESC  LIMIT  0,3 
    [{'title': '1', 'selects': 'selects'}, {'title': '1', 'selects': 'selects'}, {'title': '1', 'selects': 'selects'}]

    结果2
    SELECT `title`,`selects` FROM `demo_table` WHERE `index`>'1' ORDER BY `index` AND `title`  DESC  LIMIT  1 
    [{'title': '1', 'selects': 'selects'}]

##### 示例解释

    此ORM采用类似原生sql的方式执行对数据库表的操做，一切以你定义的POJO和对应的数据库表为标准。
    如果你使用过sql，那么一定也看得懂这类操做

#### end():

    表示本次操做已结束，可交付框架执行并返回其对应的数据：
        - POJO对象
        - 受影响行数，末尾行ID

##### 示例

    _orm = orm.find('All').end()

#### run():

    表示本次操做已结束，可交付框架执行并返回其对应的数据：
        - POJO对象
        - 受影响行数，末尾行ID

##### 示例

    _orm = orm.find('All')
    +result = _orm.run()

## 考虑到安全问题

考虑到安全问题，此ORM不提供以任何形式的 `truncate` 操做  
由于未熟读文档或操做失误导致的数据丢失均与本框架无关  
请使用前熟读文档

# 赞助商

蓝星灯塔科技有限公司

!['Blue Star DT'](./imgs/logo_tr_title.png)

CACode开发团队

!['CACode Development Team'](./imgs/icon_dev.png)
文档编辑于：2021/03/17 07:41  
作者：CACode
