"""
    Description: Filters out all poems not in the length range specified
    Example usage: python3 filter_length.py -i dataset.csv -o dataset_250.csv -m 20 -M 250
    Author: Harshit Varma
"""

import argparse
import pandas as pd
from tqdm import tqdm
from string import punctuation
from nltk.tokenize import word_tokenize

def countTokens(text):
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in punctuation]
    return len(tokens)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required = True)
    parser.add_argument("-o", "--output", required = True)
    parser.add_argument("-M", "--max_len", type = int, required = True)
    parser.add_argument("-m", "--min_len", type = int, required = True)
    args = parser.parse_args()

    PATH_IN = args.input
    PATH_OUT = args.output
    MAX_LEN = args.max_len
    MIN_LEN = args.min_len
    
    df = pd.read_csv(PATH_IN)

    tqdm.pandas()
    df["Length"] = df["Content"].progress_apply(countTokens)

    summary = df["Length"].describe()
    print(" Before: Length Statistics")
    print(summary)
    print()

    # Filter out long poems
    mask = df["Length"] <= MAX_LEN
    df = df[mask]
    # Filter out short poems
    mask = df["Length"] >= MIN_LEN
    df = df[mask]

    summary = df["Length"].describe()
    print("After: Length Statistics")
    print(summary)

    df.reset_index(drop = True, inplace = True)

    # Sort by author
    df.sort_values("Author", inplace = True)
    df.reset_index(drop = True, inplace = True)

    df.to_csv(PATH_OUT, index = False)