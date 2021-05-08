"""
    Description: Filters out all authors not in the list
    Example usage: python3 filter_authors.py -i dataset_250.csv -o dataset_250_top_authors.csv
    Author: Harshit Varma
"""

import argparse
import pandas as pd

names = [

    "Edgar Allan Poe",
    "Maya Angelou",
    "Emily Dickinson",
    "Shel Silverstein",
    "Robert Frost",
    "Pablo Neruda",
    "Langston Hughes",
    "Walt Whitman",
    "Thomas Hardy",
    "Rudyard Kipling",
    "John Keats",
    "Elizabeth Barrett Browning",
    "William Blake",
    "Sylvia Plath",
    "Henry Wadsworth Longfellow",
    "William Wordsworth",
    "Mark Twain",
    "Ralph Waldo Emerson",
    "John Donne",
    "William Butler Yeats",
    "Lord ron (George Gordon)",
    "Lewis Carroll",
    "Alfred, Lord Tennyson",
    "T. S. Eliot",
    "Ezra Pound",
    "John Milton",
    "Sappho",

    "Isaac Watts",
    "Carole Boston Weatherford",
    "George Eliot",
    "Rabindranath Tagore",
    "Christina Rossetti",
    "Robert Burns",
    "Ben Jonson",
    "Mary Mapes Dodge",
    "Joseph Brodsky",
    "Richard Wilbur",
    "Robert Graves",
    "Algernon Charles Swinburne",
]


def countPoems(df, author):
    mask = (df["Author"] == author)
    return len(df[mask]) 


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required = True)
    parser.add_argument("-o", "--output", required = True)
    args = parser.parse_args()

    PATH_IN = args.input
    PATH_OUT = args.output

    df = pd.read_csv(PATH_IN)

    print("Number of authors chosen: {}".format(len(names)))

    total = 0
    for name in names:
        n = countPoems(df, name)
        print(f"Name: {name} | Poems: {n}")
        total += n

    print(f"Number of poems by the chosen authors: {total}")

    # Select only these poems
    df = df[df["Author"].isin(names)]

    df.reset_index(drop = True, inplace = True)
    df.to_csv(PATH_OUT, index = False)