"Wheeeee"
import index
from .. import app

@index.app.route("/api/v1/", methods=["GET"])
def root():
    """GET /api/v1/."""
    return {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }