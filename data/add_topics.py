"""
    Description: Adds the topics column suing extract_topics.py
    Example usage: python3 add_topics.py -i dataset.csv -o dataset_with_topics.csv -s stopwords/stopwords.txt
    Author: Harshit Varma
"""

import random
import argparse
from string import punctuation

import pandas as pd
from tqdm import tqdm

from extract_topics import TopicExtractor

random.seed(0)

def getTopicList(text, sep = ", ", n_min = 7, n_max = 15):

    topics = te.extract(text, seed = 0)
    n_topics = random.randint(n_min, n_max)

    if len(topics) > n_topics:
        topics = topics[:n_topics] # prefer bigrams over unigrams

    topics = sep.join(topics)

    return topics


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required = True)
    parser.add_argument("-o", "--output", required = True)
    parser.add_argument("-s", "--stopwords", required = True)
    args = parser.parse_args()

    PATH_IN  = args.input
    PATH_OUT = args.output
    PATH_SW  = args.stopwords
 
    df = pd.read_csv(PATH_IN)

    te = TopicExtractor(PATH_SW, punctuation)

    tqdm.pandas()
    df["Topics"] = df["Content"].progress_apply(getTopicList)

    df.to_csv(PATH_OUT, index = False)