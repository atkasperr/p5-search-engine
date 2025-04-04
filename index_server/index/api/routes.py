"""Meow."""
import index
from flask import jsonify, request
import re
from .. import app

# Index data
stopwords = set()
inverted_index = {}
pagerank = {}

def load_index(app):
    """Load the data into the lists called in index/__init__."""
    global inverted_index, pagerank, stopwords

    # Load inverted index
    with open(app.config["INDEX_PATH"], "r") as f:
        for line in f:
            parts = line.strip().split()
            inverted_index[parts[0]] = parts[1:]

    # Load PageRank
    with open(app.config["PAGERANK_PATH"], "r") as f:
        for line in f:
            docid, score = line.strip().split(',')
            pagerank[docid] = float(score)

    # Load the stopwords
    with open(app.config["STOPWORDS_PATH"], "r") as f:
        for line in f:
            stopwords.update(line.strip() for line in f) 


@app.route("/api/v1/hits", methods=["GET"])
def get_hits():
    """Return hits."""
    query = request.args.get("q", "")
    weight = request.args.get("w", 0.5)

    # clean the query (from the inverted_index part of spec)
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", "", query)
    terms = [t for t in cleaned.split() if t not in stopwords]

    results = []

    # Calculate scores
    for term in terms:
        if term in inverted_index:
            data = inverted_index[term]
            idf = float(data[0])
            
            # Process each document entry (docid, tf, norm)
            for i in range(1, len(data), 3):
                docid = data[i]
                tf = int(data[i+1])
                norm = float(data[i+2])
                # TF-IDF score
                tfidf = (tf * idf) / norm
                
                # Get PageRank score (default to 0 if missing)
                pr = pagerank.get(docid, 0.0)
                
                # Combine scores
                score = (1 - weight) * tfidf + weight * pr
                results.append({
                    "docid": int(docid),
                    "score": round(score, 6)
                })

    # Sort and return top 10
    results.sort(key=lambda x: -x["score"])
    return jsonify({"hits": results[:10]})