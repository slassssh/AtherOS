class PluginCommunication:


    def send(self, source, target):

        return {
            "source": source,
            "target": target,
            "sent": True
        }