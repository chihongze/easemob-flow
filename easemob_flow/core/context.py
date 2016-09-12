import collections
from abc import ABCMeta


class AbstractFlowContext(collections.Mapping, metaclass=ABCMeta):

    """上下文对象用于在Flow运行中的Job之间传递数据
    """

    def __init__(self):
        super().__init__()

    def init(self):
        pass

    def destroy(self):
        pass


class MySQLContext(AbstractFlowContext):

    """基于MySQL的上下文
    """

    def __init__(self, db, flow_instance_id):
        self._db = db
        self._flow_instance_id = flow_instance_id

    def __getitem__(self, key):
        return self._db.query_one_field((
            "select v from flow_context where "
            "flow_instance_id = %s and k = %s"
        ), (self._flow_instance_id, key))

    def __setitem__(self, key, value):
        self._db.execute((
            "insert into flow_context ("
            "flow_instance_id, k, v) values ("
            "%s, %s, %s) on duplicate key update "
            "v = %s"
        ), (self._flow_instance_id, key, value, value))

    def __delitem__(self, key):
        return self._db.execute((
            "delete from flow_context where "
            "flow_instance_id = %s and k = %s limit 1"
        ), (self._flow_instance_id, key))

    def __len__(self):
        return self._db.query_one_field((
            "select count(*) as c from flow_context where "
            "flow_instance_id = %s"
        ), (self._flow_instance_id,))

    def __iter__(self):
        return self.keys()

    def get(self, key):
        return self[key]

    def items(self):
        rs = self._db.query_all((
            "select k, v from flow_context where "
            "flow_instance_id = %s"
        ), (self._flow_instance_id,))
        return [(row["k"], row["v"]) for row in rs]

    def keys(self):
        rs = self._db.query_all((
            "select k from flow_context where "
            "flow_instance_id = %s"
        ), (self._flow_instance_id,))
        return [row['k'] for row in rs]

    def values(self):
        rs = self._db.query_all((
            "select v from flow_context where "
            "flow_instance_id = %s"
        ), (self._flow_instance_id,))
        return [row['v'] for row in rs]

    def destroy(self):
        self._db.execute((
            "delete from flow_context where "
            "flow_instance_id = %s"
        ), (self._flow_instance_id,))
