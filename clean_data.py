import pandas as pd

def cleanTitles(text):
    text = text.strip('"') # Remove all "
    text = text.strip("'") # Remove all '
    text = text.strip('(') # Remove all (
    text = text.strip(')') # Remove all )
    text = text.strip('“')
    text = text.strip('”')
    return text

df = pd.read_csv("kaggle_poem_dataset.csv", index_col = 0, encoding = "utf-8")

df["Title"] = df["Title"].apply(cleanTitles)

df.sort_values("Title", inplace = True)
df.reset_index(drop = True, inplace = True)

# Delete a few initial and ending rows as these contain mostly garbage data
df = df.iloc[40:]
df = df.iloc[:-100]
df.reset_index(drop = True, inplace = True)

df.to_csv("dataset.csv", index = False)
