"""..."""
from flask import Flask
import os
from pathlib import Path
# import index.api


app = Flask(__name__)
# Load inverted index, stopwords, and pagerank into memory
# index.api.load_index()

INDEX_DIR = Path(__file__).parent/"inverted_index"
app.config["INDEX_PATH"] = os.getenv(
    "INDEX_PATH", # Environment variable name
    INDEX_DIR/"inverted_index_1.txt"  # Default value
)
app.config["PAGERANK_PATH"] = str(Path(__file__).parent / "pagerank.out")
app.config["STOPWORDS_PATH"] = str(Path(__file__).parent / "stopwords.txt")

# import stuff here
# from .api import routes
import index.api
index.api.load_index(app)