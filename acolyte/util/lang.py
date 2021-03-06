"""本模块包含语言增强方面的工具
"""


def to_str(obj, *fields):
    """该函数用于方便生成__repr__和__str__方法的返回内容
       :param obj: 目标对象
       :param fields: 目标属性，如果不指定，则会返回所有
    """

    # if fields is empty, auto get fields
    if not fields:
        try:
            fields = obj.__dict__.keys()
        except AttributeError:
            # maybe slots class
            fields = obj.__slots__

    str_buf = [
        "{class_name}@{id_} <",
    ]
    for idx, field in enumerate(fields):

        if isinstance(field, str):
            # 单纯str
            str_buf.append("{field}={value}".format(
                field=field, value=getattr(obj, field)))
        elif isinstance(field, tuple):
            # 包含callback处理
            field, callback = field
            str_buf.append("{field}={value}".format(
                field=field, value=callback(getattr(obj, field))))
        else:
            # 其它类型不支持
            raise AttributeError("Unsupport field type: '{clazz}'".format(
                clazz=field.__class__.__name__))

        if idx < len(fields) - 1:
            str_buf.append(", ")

    str_buf.append(">")
    return "".join(str_buf).format(
        class_name=obj.__class__.__name__,
        id_=id(obj)
    )


def get_from_nested_dict(d, *keys, default=None):
    """从嵌套字典中获取值，如果在某一层级获取不到，则返回None
       :param d: 目标字典
       :param keys: 层级key列表
    """
    for k in keys:
        try:
            d = d[k]
        except KeyError:
            return default
    return d


def get_full_class_name(cls):
    """获取一个类的完整名称 包名.类名
    """
    return cls.__module__ + "." + cls.__name__
