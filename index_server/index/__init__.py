"""..."""
from flask import Flask
import os
from pathlib import Path
import index.api  # noqa: E402  pylint: disable=wrong-import-position


app = Flask(__name__)
# Load inverted index, stopwords, and pagerank into memory
index.api.load_index()

app.config["INDEX_PATH"] = os.getenv(
    "INDEX_PATH",
    str(Path(__file__).parent / "inverted_index/part-00000") 
)
app.config["PAGERANK_PATH"] = str(Path(__file__).parent / "pagerank.out")
app.config["STOPWORDS_PATH"] = str(Path(__file__).parent / "stopwords.txt")

# import stuff here
import api