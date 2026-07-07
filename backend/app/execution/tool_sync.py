class ToolExecutionSync:


    def execute_tool(self, tool, payload):

        return {
            "tool": tool,
            "payload": payload,
            "executed": True
        }