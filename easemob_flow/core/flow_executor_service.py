from easemob_flow.util.service_container import ServiceContainer
from easemob_flow.core.service import (
    AbstractService,
    Result,
)
from easemob_flow.core.storage.flow_template import (
    FlowTemplateDAO,
)


class FlowExecutorService(AbstractService):

    def __init__(self, service_container: ServiceContainer):
        super().__init__("flow_executor_service", service_container)

    def _after_register(self):
        # 获取各种所依赖的服务
        self._flow_tpl_dao = FlowTemplateDAO(self.service("db"))
        self._flow_meta_mgr = self.service("flow_meta_manager")
        self._job_mgr = self.service("job_manager")

    def start_flow(self, flow_template_id: int,
                   start_flow_args: dict,
                   first_job_trigger_args: dict) -> Result:
        """开启一个flow进程，创建flow_instance并执行第一个Job

           S1. 根据flow_template_id获取flow_template，然后获取flow_meta，如果获取失败，返回错误
           S2. 检查max_run_instance
           S3. 创建一条新的flow_instance记录
           S4. 回调flow meta中on_start方法的逻辑
           S5. 回调第一个Job的trigger事件

           :param flow_name: 具体的flow_template的名称
           :param first_job_trigger_args: 触发第一个Job需要的参数
           :return flow_instance
        """
        flow_template = self._flow_tpl_dao.query_flow_template_by_id(
            flow_template_id)
        if flow_template is None:
            return Result.bad_request(
                "template_not_found",
                msg=self.msg(tpl_id=flow_template_id))

    def next_job(self, flow_instance_id: int, current_job_finish_args: dict,
                 new_job_trigger_args: dict) -> Result:
        """执行下一个Job
           :param flow_instance_id: flow的标识，可以是flow_template或者flow_instance_id
           :param current_job_finish_args: 用于结束当前Job的参数
           :param new_job_trigger_args: 用于触发新Job的参数
           :return job_instance
        """
        pass

    def handle_job_action(self, flow_instance_id: int, job_action: str,
                          action_args: dict) -> Result:
        """处理Job中的自定义动作
           :param flow_instance_id: flow的标识
           :param job_action: 自定义的动作名称
           :param action_args: 执行该自定义动作所需要的参数
        """
        pass

    def stop(self, flow_instance_id: int, stop_flow_args: dict,
             stop_job_args: dict) -> Result:
        """终止flow
           :param flow_instance_id flow的标识
           :param stop_args 终止参数
        """
        pass
