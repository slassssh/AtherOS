class WindowManager:


    def __init__(self):

        self.windows = []



    def create_window(self, name):

        self.windows.append(
            name
        )

        return {
            "window": name,
            "created": True
        }



    def list_windows(self):

        return self.windows