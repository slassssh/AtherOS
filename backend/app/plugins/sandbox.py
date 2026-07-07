class PluginSandbox:


    def isolate(self, plugin):

        return {
            "plugin": plugin,
            "sandboxed": True
        }