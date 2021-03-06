"""本模块包含跟Job相关的Facade接口
"""

from acolyte.core.service import AbstractService


class JobService(AbstractService):

    def __init__(self, service_container):
        super().__init__(service_container)

    def get_all_job_definations(self):
        """获取所有的Job定义
        """
        pass

    def get_job_instance_list_by_flow_instance(self, flow_instance_id):
        """根据flow_instance_id获取job_instance列表
        """
        pass

    def get_job_instance_details(self, job_instance_id):
        """获取某个job_instance的详情数据，包括每个其中每个event的数据
        """
        pass
