class ThemeEngine:


    def __init__(self):

        self.theme = "dark"



    def set_theme(self, theme):

        self.theme = theme

        return True



    def current(self):

        return self.theme