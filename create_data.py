import pandas as pd
from tqdm import tqdm

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from rake_nltk import Rake

SW = stopwords.words("english")
extractor = Rake(SW)

df = pd.read_csv("dataset_150.csv")

def getTopicList(text, sep = "\n", max_topics = 10):
    # tokens = word_tokenize(text)
    # cleaned = [w for w in tokens if w not in SW]
    # cleaned_text = " ".join(cleaned)
    extractor.extract_keywords_from_text(text)
    kw = extractor.get_ranked_phrases()
    if len(kw) > max_topics:
        kw = kw[:max_topics] 
    kw = sep.join(kw)
    return kw

tqdm.pandas()
df["Topics"] = df["Content"].progress_apply(getTopicList)

df.to_csv("poem_topics_150.csv", index = False)