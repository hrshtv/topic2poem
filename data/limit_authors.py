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

]


def countPoems(df, author):
    mask = (df["Author"] == author)
    return len(df[mask]) 


if __name__ == '__main__':

    data_path = "dataset_200.csv"

    print("Number of authors chosen: {}".format(len(names)))

    df = pd.read_csv(data_path)

    total = 0
    for name in names:
        n = countPoems(df, name)
        print(f"Name: {name} | Poems: {n}")
        total += n

    print(f"Number of poems by the chosen authors: {total}")

    # Select only these poems
    df = df[df["Author"].isin(names)]

    df.reset_index(drop = True, inplace = True)
    df.to_csv("dataset_200_top_authors.csv", index = False)