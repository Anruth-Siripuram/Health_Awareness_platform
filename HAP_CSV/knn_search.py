from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

def knn_search(query, df):
    df = df.copy()
    df["text_features"] = df["title"].fillna("") + " " + df["symptoms"].fillna("") + " " + df["overview"].fillna("")
    tfidf = TfidfVectorizer(stop_words="english")
    X = tfidf.fit_transform(df["text_features"])

    n_samples = X.shape[0]
    n_neighbors = min(5, n_samples)  # <-- ensure n_neighbors <= samples
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine")
    knn.fit(X)

    q_vec = tfidf.transform([query])
    distances, indices = knn.kneighbors(q_vec)
    return df.iloc[indices[0]]
