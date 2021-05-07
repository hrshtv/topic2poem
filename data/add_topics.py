import random
from string import punctuation

import pandas as pd
from tqdm import tqdm

from extract_topics import TopicExtractor

def clean(text):
    text = text.replace("’", "'")
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    return text

def getTopicList(text, sep = ", "):

    topics = te.extract(text)
    n_topics = random.randint(7, 15)

    if len(topics) > n_topics:
        topics = topics[:n_topics] # prefer bigrams over unigrams

    topics = sep.join(topics)

    return topics


if __name__ == '__main__':

    df = pd.read_csv("dataset_200_top_authors.csv")

    te = TopicExtractor("stopwords.txt", punctuation)

    tqdm.pandas()

    print("Cleaning:")
    df["Content"] = df["Content"].progress_apply(clean)

    print("Extracting topics:")
    df["Topics"] = df["Content"].progress_apply(getTopicList)

    df.to_csv("poem_topics_200_top_authors.csv", index = False)