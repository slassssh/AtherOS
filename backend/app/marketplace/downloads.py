class DownloadsTracker:


    def __init__(self):

        self.count = 0



    def download(self):

        self.count += 1


        return {
            "downloads": self.count
        }