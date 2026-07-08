class ReviewsSystem:


    def __init__(self):

        self.reviews = []



    def add(self, review):

        self.reviews.append(review)

        return True



    def all(self):

        return self.reviews