class RetryPolicy:


    def __init__(self, retries=3):

        self.retries = retries


    def attempt(self, function):

        for _ in range(
            self.retries
        ):

            try:

                return function()

            except Exception:

                continue


        return None