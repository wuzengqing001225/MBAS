from SABM.Utils.Text_Processing import format_prompt
from SABM.Utils.Text_Processing import format_response
from SABM.Utils.Implement_Tools import display
from SABM.Utils.Text_Processing import calculation
from SABM.Data import agent_settings
import textwrap

class company():
    def __init__(self, id, n_agents, job_type, type = "Company"):
        # Static Properties
        self.n_agents = n_agents
        self.id = id
        self.job_type = job_type
        self.type = type
        self.max_member = self.update_max_member()

        # Dynamic Properties
        self.salary = self.update_salary()
        self.company_type = self.init_company_type() # Company gender type
        self.member_id = []
        self.NVratio = 0

        # History
        self.member_number_history = []
        self.salary_history = []
        self.NVratio_history = []
    
    def info_display(self):
        member_list = format_prompt.format_list(self.member_id)
        if member_list in [None, ""]: member_list = "None"

        info = f"""
            {self.type}
            [Job Type] {self.job_type}
            [Max Member] {self.max_member}
            [Salary] {self.salary}
            [Current Member] {self.calu_current_member()}
            [Current Member ID] {member_list}"""
        print(textwrap.dedent(info))
    
    def calu_current_member(self):
        return len(self.member_id)
    
    def update_max_member(self):
        if agent_settings.job_data[self.job_type][3] > 1 or agent_settings.job_data[self.job_type][3] < 0: agent_settings.job_data[self.job_type][3] = 1
        return int(agent_settings.job_data[self.job_type][3] * self.n_agents)
    
    def update_salary(self):
        if agent_settings.job_data[self.job_type][2] < 0: agent_settings.job_data[self.job_type][2] = 1000
        return agent_settings.job_data[self.job_type][2]
    
    def update_member(self):
        self.member_id = sorted(self.member_id)

    def init_company_type(self):
        return agent_settings.job_data[self.job_type][0]

    def remove_member(self, id_to_remove):
        #self.member_id = [x for x in self.member_id if x != id_to_remove]
        self.member_id.remove(id_to_remove)
        self.update_member()
