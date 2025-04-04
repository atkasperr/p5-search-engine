"""Meow"""
import index

@index.route("/api/v1/", methods=["GET"])
def get_services():
    """GET /api/v1/"""
    return {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }