import pandas as pd
from tqdm import tqdm
from string import punctuation
from nltk.tokenize import word_tokenize

MAX_LEN = 200

def countTokens(text):
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in punctuation]
    return len(tokens)

if __name__ == '__main__':
    
    df = pd.read_csv("dataset.csv")

    tqdm.pandas()
    df["Length"] = df["Content"].progress_apply(countTokens)

    summary = df["Length"].describe()

    """
    Original length statistics:
    count    15512.000000
    mean       266.748002
    std        527.133714
    min          1.000000
    25%        104.000000
    50%        160.000000
    75%        276.000000
    max      24091.000000
    """

    mask = df["Length"] <= MAX_LEN
    df = df[mask]

    df.reset_index(drop = True, inplace = True)

    df.to_csv(f"dataset_{MAX_LEN}.csv", index = False)