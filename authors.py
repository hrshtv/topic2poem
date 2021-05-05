import pandas as pd

data_path = "dataset_200.csv"
# data_path = "poem_topics_improved_bigrams_150.csv" # 413 poems

# source: https://www.deseret.com/2015/3/20/20479016/poets-famous-quotes-birthplace-writers-edgar-allen-poe-maya-angelou-emily-dickinson
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

names = list(set(names)) # just a sanity check

print(len(names))

df = pd.read_csv(data_path)

def countPoems(df, author):
    mask = df["Author"] == author
    return len(df[mask]) 

total = 0
for name in names:
    n = countPoems(df, name)
    print(f"Name: {name} | Poems: {n}")
    total += n

print(total)

# Select only these poems
df = df[df["Author"].isin(names)]
print(df)

df.reset_index(drop = True, inplace = True)
df.to_csv("dataset_200_top_authors.csv", index = False)