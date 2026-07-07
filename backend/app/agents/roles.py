class AgentRoles:


    def __init__(self):

        self.roles = {}


    def assign(self, agent_id, role):

        self.roles[agent_id] = role

        return True


    def get_role(self, agent_id):

        return self.roles.get(agent_id)