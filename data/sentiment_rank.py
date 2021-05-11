from nltk.sentiment.vader import SentimentIntensityAnalyzer

topics = [
    "spirit walks", 
    "eternal process", 
    "lower life", 
    "human worth", 
    "shattered stalks",
    "weeping tree",
    "elated smile",
    "happy faces",
    "gilded armour",
]

sia = SentimentIntensityAnalyzer()

def sentiRank(topics):
    topic_scores = []
    for t in topics:
        scores_dict = sia.polarity_scores(t)
        del scores_dict["compound"]
        stype = max(scores_dict, key = scores_dict.get)
        sval = scores_dict[stype]
        if stype == "neu":
            topic_scores.append((0, sval))
        else:
            topic_scores.append((1, sval))
    # Sort by topic scores
    ranked_topics = [t for _, t in sorted(zip(topic_scores, topics), reverse = True)]
    return ranked_topics

print(sentiRank(topics))