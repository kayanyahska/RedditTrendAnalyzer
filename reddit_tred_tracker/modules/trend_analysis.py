from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def analyze_trends(posts):
    texts = []
    scores = []
    for post in posts:
        if post.get("selftext"):
            texts.append(post["title"] + " " + post["selftext"])
            scores.append(post["score"])

    if not texts:
        return {"error": "No text content available for analysis.", "total_posts": len(posts)}

    sentiments = [sia.polarity_scores(t)["compound"] for t in texts]

    vectorizer = CountVectorizer(stop_words="english", max_features=1000)
    X = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(n_components=3, random_state=42)
    lda.fit(X)

    topics = []
    for i, topic in enumerate(lda.components_):
        top_words = [vectorizer.get_feature_names_out()[j] for j in topic.argsort()[:-6:-1]]
        topics.append({"topic_id": i, "keywords": top_words})

    clusters = []
    if len(texts) >= 3:
        km = KMeans(n_clusters=3, random_state=0).fit(X)
        clusters = km.labels_.tolist()

    sentiment_summary = {
        "positive": sum(s > 0.2 for s in sentiments),
        "neutral": sum(-0.2 <= s <= 0.2 for s in sentiments),
        "negative": sum(s < -0.2 for s in sentiments),
    }

    regression = {}
    if len(texts) > 3:
        model = LinearRegression()
        model.fit(X.toarray(), scores)
        feature_names = vectorizer.get_feature_names_out()
        regression = {
            "coef": model.coef_.tolist(),
            "intercept": model.intercept_,
            "r2": model.score(X.toarray(), scores),
            "features": feature_names.tolist()  # 👈 Add this line
        }

    return {
        "topics": topics,
        "sentiment_summary": sentiment_summary,
        "clusters": clusters,
        "regression": regression,
        "total_posts": len(posts)
    }
