import pandas as pd
from tqdm import tqdm

df = pd.read_csv("dataset_200_top_authors.csv")

def clean(text):
    text = text.replace("’", "'")
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    return text

tqdm.pandas()
df["Content"] = df["Content"].progress_apply(clean)

df.to_csv("dataset_200_top_authors.csv", index = False)