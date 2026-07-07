class CommentsSystem:


    def __init__(self):

        self.comments = []



    def add(self, comment):

        self.comments.append(comment)

        return True



    def all(self):

        return self.comments