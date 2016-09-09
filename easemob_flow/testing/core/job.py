import simplejson as json
import traceback
from easemob_flow.core.job import AbstractJob, JobArg


class EchoJob(AbstractJob):

    """该Job用于测试，打印事件和参数，并返回接收到的参数
    """

    def __init__(self):
        super().__init__("echo", "test job echo", job_args={
            "trigger": [
                JobArg("a", JobArg.TYPE_INT, "a的值"),
                JobArg("b", JobArg.TYPE_INT, "b的值"),
            ],
            "finish": [
                JobArg("c", JobArg.TYPE_STRING, "c的值"),
                JobArg("d", JobArg.TYPE_LIST, "d的值")
            ],
            "stop": [
                JobArg("e", JobArg.TYPE_FLOAT, "e的值"),
                JobArg("f", JobArg.TYPE_DICT, "f的值")
            ],
        })

    def on_trigger(self, context, arguments):
        print("on trigger events, received args: {}".format(
            json.dumps(arguments)))
        return arguments

    def on_finish(self, context, arguments):
        print("on finish events, received args: {}".format(
            json.dumps(arguments)))
        return arguments

    def on_stop(self, context, arguments):
        print("on stop events, received args: {}".format(
            json.dumps(arguments)))
        return arguments

    def on_exception(self, context, exc_type, exc_value, tb):
        traceback.print_exception(exc_type, exc_value, tb)


class OldManJob(AbstractJob):

    """Mock Job 长者Job
    """

    def __init__(self):
        super().__init__("old_man", "old man job")

    def on_trigger(self, context, arguments):
        print("任何事情都要按照基本法，按照选举法！我没有要钦定！没有任何这个意思！")
        return "trigger"

    def on_finish(self, context, arguments):
        print("I'm angry!")
        return "finish"

    def on_stop(self, context, arguments):
        print("你们啊！naive！")
        return "stop"

    def on_xxx(self, context, arguments):
        print("你们这样子是不行的！我也是替你们捉急！")
        return "xxx"

    def on_exception(self, context, exc_type, exc_value, tb):
        print("跑的比谁都快！")
        return "exception"


def letter_job_meta(letter):

    class LetterJobMeta(type):

        def __new__(cls, name, bases, attrs):

            def _make_method(action):
                def method(self, context, arguments):
                    print("{action}: {letter}".format(
                        action=action, letter=letter))
                    return "{action}_{letter}".format(
                        action=action, letter=letter)
                return method

            attrs["on_trigger"] = _make_method("trigger")
            attrs["on_finish"] = _make_method("finish")
            attrs["on_stop"] = _make_method("stop")
            attrs["on_exception"] = \
                lambda self, context, exc_type, exc_value, tb: "exception"
            attrs["__init__"] = lambda self: AbstractJob.__init__(
                self, "job_" + letter, "job " + letter)

            bases += (AbstractJob,)

            return type(name, bases, attrs)

    return LetterJobMeta


class AJob(metaclass=letter_job_meta("A")):
    pass


class BJob(metaclass=letter_job_meta("B")):
    pass


class CJob(metaclass=letter_job_meta("C")):
    pass


class DJob(metaclass=letter_job_meta("D")):
    pass
