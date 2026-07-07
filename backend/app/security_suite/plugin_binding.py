class PluginSecurityBinding:


    def bind(self, plugin):

        return {
            "plugin": plugin,
            "secured": True
        }