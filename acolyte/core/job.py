import datetime
from typing import (
    Dict,
    Any
)
from abc import (
    ABCMeta,
    abstractmethod
)
from acolyte.util.validate import Field


class AbstractJob(metaclass=ABCMeta):

    """描述一个Job
       实现的其它Job均需要继承该类
    """

    def __init__(self, name: str, description: str,
                 job_args: Dict[str, Any]=None):
        """
        :param name: Job名称
        :param description: Job描述
        :param job_args: Job参数声明
        """
        self._name = name
        self._description = description
        self._job_args = job_args if job_args is not None else {}

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def job_args(self):
        return self._job_args

    @abstractmethod
    def on_trigger(self, context, arguments):
        """当工作单元被触发时执行此动作
        """
        pass


class JobStatus:

    """Job实例的各种运行状态
    """

    STATUS_WAITING = "waiting"

    STATUS_RUNNING = "running"

    STATUS_FINISHED = "finished"

    STATUS_STOPPED = "stopped"

    STATUS_EXCEPTION = "exception"


class JobInstance:

    """描述一个Job的运行状态
    """

    def __init__(self, id_: int, flow_instance_id: int, step_name: str,
                 status: str, trigger_actor: int, created_on, updated_on):
        """
        :param id_: 每个Job的运行实例有一个编号
        :param flow_instance_id: 隶属的flow_instance
        :param step_name: step名称
        :param status: 运行状态
        :param trigger_actor: 触发者
        :param created_on: 运行实例起始时间
        :param updated_on: 最近更新状态时间
        """
        self.id = id_
        self.flow_instance_id = flow_instance_id
        self.step_name = step_name
        self.status = status
        self.trigger_actor = trigger_actor
        self.created_on = created_on
        self.updated_on = updated_on


class JobActionData:

    """记录Job每一个Action执行的数据
    """

    def __init__(self,
                 id_: int, job_instance_id: int,
                 action: str, actor: int,
                 arguments: Dict[str, Any],
                 data: Dict[str, Any],
                 created_on: datetime.datetime,
                 updated_on: datetime.datetime):
        """
        :param id_: Action实例编号
        :param job_instance_id: 隶属的job instance
        :param action: 动作名称
        :param actor: 执行者
        :param arguments: 执行该Action时所使用的参数
        :param data: 该Action执行后回填的数据
        :param created_on: 执行时间
        :param finished_on: 执行结束时间
        """

        self.id = id_
        self.job_instance_id = job_instance_id
        self.action = action
        self.actor = actor
        self.arguments = arguments
        self.data = data
        self.created_on = created_on
        self.updated_on = updated_on


class JobRef:

    """还对象用于在FlowMeta等声明中引用一个Job
    """

    def __init__(self, step_name: str, job_name: str, **bind_args):
        """
        :param step_name: 不能叫'start'或者'finish'，这俩是保留字
        """
        self._step_name = step_name
        self._job_name = job_name
        self._bind_args = bind_args if bind_args is not None else {}

    @property
    def step_name(self):
        return self._step_name

    @property
    def job_name(self):
        return self._job_name

    @property
    def bind_args(self):
        return self._bind_args


class JobArg:

    """参数声明
    """

    # 参数类型

    MARK_AUTO = "auto"  # 自动变量，绑定参数值可以被运行时参数值所覆盖

    MARK_CONST = "const"  # const类型的参数的值自FlowMeta指定后就不在变了

    MARK_STATIC = "static"  # static类型的参数值自FlowInstance指定后就不再变了

    def __init__(self, name: str,
                 field_info: Field, mark: str, comment: str):
        """
        :param step_name: 当前步骤名称
        :param job_name: 引用的job名称
        :param field_info: 字段类型以及验证属性
        :param mark: 字段标记 auto、const、static
        :param comment: 说明
        """
        self._name = name
        self._field_info = field_info
        self._mark = mark
        self._comment = comment

    @property
    def name(self):
        return self._name

    @property
    def field_info(self):
        return self._field_info

    @property
    def mark(self):
        return self._mark

    @property
    def comment(self):
        return self._comment
