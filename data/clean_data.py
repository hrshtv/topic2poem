"""
    Description: Cleans the data downloaded from https://www.kaggle.com/johnhallman/complete-poetryfoundationorg-dataset 
    Example usage: python3 clean_data.py -i kaggle_poem_dataset.csv -o dataset.csv
    Author: Harshit Varma
"""

import string
import argparse
import pandas as pd
from tqdm import tqdm

# Reference: https://learn.lexiconic.net/shakewords.htm
archaic_dict = {

    "'d" : "ed",
    "e'er" : "ever", 
    "'ere" : "before",
    "o'er" : "over",
    "'tis" : "it is",
    "'twas" : "it was",

    " oft " : " often ",
    " hie " : " hurry "

}

def clean(text):

    # Single inverted commas
    text = text.replace("‘", "'")
    text = text.replace("’", "'")
    # Double inverted commas
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    # Hyphens
    text = text.replace("‐", "-")
    text = text.replace("᠆", "-")
    text = text.replace("᠆", "-")
    text = text.replace("－", "-")
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = text.strip(string.punctuation)

    for w1, w2 in archaic_dict.items():
        text = text.replace(w1, w2)
        text = text.replace(w1.capitalize(), w2)

    return text


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required = True)
    parser.add_argument("-o", "--output", required = True)
    args = parser.parse_args()

    PATH_IN = args.input
    PATH_OUT = args.output
    
    df = pd.read_csv(PATH_IN, index_col = 0, encoding = "utf-8")

    # Clean titles and content
    tqdm.pandas()
    df["Title"] = df["Title"].progress_apply(clean)
    df["Content"] = df["Content"].progress_apply(clean)

    # Sort by title
    df.sort_values("Title", inplace = True)
    df.reset_index(drop = True, inplace = True)

    df.to_csv(PATH_OUT, index = False)
