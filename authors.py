import pandas as pd

data_path = "poem_topics_improved_bigrams_150.csv"

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
    "Oscar Wilde",
    "John Keats",
    "Elizabeth Barrett Browning",
    "William Blake",
    "Sylvia Plath",
    "Henry Wadsworth Longfellow",
    "William Wordsworth",
    "Mark Twain",
    "Ralph Waldo Emerson",
    "John Donne",
    "W.B. Yeats",
    "Lord Byron",
    "Lewis Carroll",
    "Alfred, Lord Tennyson",
    "T.S. Eliot",
    "Ezra Pound",
    "John Milton",
    "Sappho",
    "Homer",
    "Li Bai",
]

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