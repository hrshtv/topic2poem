import random
from string import punctuation

import pandas as pd
from tqdm import tqdm

from extract_topics import TopicExtractor

df = pd.read_csv("dataset_150.csv")

punctuation = [p for p in punctuation]
punctuation += ["—", "*", "’"]
te = TopicExtractor("stopwords.txt", punctuation)

def getTopicList(text, sep = "\n"):

    topics = te.extract(text)
    n_topics = random.randint(7, 15)

    if len(topics) > n_topics:
        topics = topics[:n_topics] # prefer bigrams over unigrams, already randomly sorted topics, no need to sample

    topics = sep.join(topics)

    return topics

tqdm.pandas()
df["Topics"] = df["Content"].progress_apply(getTopicList)

df.to_csv("poem_topics_improved_bigrams_150.csv", index = False)