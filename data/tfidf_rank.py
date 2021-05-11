import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("topics_250_top_authors.csv")

corpus = df["Content"].tolist()

# Load the stopwords from a file
with open("stopwords.txt", "r", encoding = "utf-8") as f:
    sw = f.readlines()
sw = [w.strip() for w in sw[1:]] # Skip the first line
# punctuation = [p for p in punctuation]
# sw += punctuation

vectorizer = TfidfVectorizer(
    decode_error = "ignore",
    strip_accents = "ascii",
    lowercase = True,
    stop_words = sw,
    ngram_range = (1, 2),
)

S = vectorizer.fit_transform(corpus)

df = pd.DataFrame(S.toarray(), columns = vectorizer.get_feature_names())
print(df)

row = df.iloc[0]
for c in row:
    print(c)
print(df.iloc[0]["eternal process"])
print(df.iloc[0]["lower life"])
print(df.iloc[0]["shattered stalks"])
print(df.iloc[0]["human worth"])