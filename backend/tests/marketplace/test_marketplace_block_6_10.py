import os
import sys


sys.path.append(
    os.path.abspath(".")
)


from backend.app.marketplace.publisher import PublisherSystem
from backend.app.marketplace.ratings import RatingsSystem
from backend.app.marketplace.reviews import ReviewsSystem
from backend.app.marketplace.downloads import DownloadsTracker
from backend.app.marketplace.version import VersionManager



def test_marketplace_ecosystem():


    assert PublisherSystem().publish(
        "plugin"
    )["published"]



    assert RatingsSystem().rate(
        "plugin",
        5
    )["rating"] == 5



    reviews = ReviewsSystem()

    reviews.add(
        "great"
    )


    assert "great" in reviews.all()



    downloads = DownloadsTracker()

    assert downloads.download()["downloads"] == 1



    assert VersionManager().set(
        "1.0"
    )["active"]




if __name__ == "__main__":

    test_marketplace_ecosystem()


    print(
        "✅ Phase 22 Block 2 (Features 6-10) Marketplace Tests Passed"
    )