# topic2poem
End-to-End Poetry Generation from a list of topics using [T5: Text-To-Text Transfer Transformer](https://arxiv.org/abs/1910.10683)

## Usage
All code is present in `code/main.ipynb` (opening this in [Google Colab](https://colab.research.google.com/) is preferable)

## Data

### Creating the Dataset
- Download the [Poetry Foundation](https://www.poetryfoundation.org/) dataset from [Kaggle](https://www.kaggle.com/johnhallman/complete-poetryfoundationorg-dataset)
- Clone this repository and place the downloaded `csv` file in `data/`
- `cd` to `data/` and run `bash pipeline.sh`

### Details
- First, `data/clean_data.py` is executed, which replaces some non-ascii punctuations by their ascii version and also replaces some common archaic words by their modern english versions
- After this, `data/filter_length.py` is executed, which keeps only the poems of length (in tokens) between `[50, 250]` and discards the rest
- Then, `data/filter_authors.py` is executed, which keeps only the poems written by a particular set of authors, specified in the file itself
- After this, `data/add_topics.py` is executed which generates the list of topics for each poem using `data/extract_topics.py`
The number of topics extracted for a given poem is sampled uniformly from `[10, 15]`

### Topic Extraction and Ranking
A 'topic' here refers to a unigram or a bigram which is present in the text  
The code for extracting and ranking is present in `data/extract_topics.py`

#### Extraction
- The given text is first labelled using [POS tagging](https://en.wikipedia.org/wiki/Part-of-speech_tagging), using [NLTK](https://www.nltk.org/api/nltk.tag.html#nltk.tag.perceptron.PerceptronTagger)
- Then, unigrams that are in `["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS", "VBG"]` are classfied as topics
- For each noun (`["NN", "NNS", "NNP", "NNPS"]`) in the topics, if the previous token lies in `["JJ", "JJR", "JJS", "NN"]`, 
then the bigram formed after combining the two unigrams (i.e the previous token and the noun) is added to the topics, 
and the individual unigrams are removed from the topics (if they were added before)

#### Ranking
- Using [VADER](https://www.nltk.org/_modules/nltk/sentiment/vader.html), each topic's sentiment scores (`pos, neg, neu`) are obtained
- Each topic is assigned a tuple of the form `(pref, val)`
  - `val` is the maximum of the three sentiments 
  - `pref` is `0` if `val` corresponds to `neu` else it's `1`, this leads to positive and negative topics having equal preference and being preferred over neutral topics 
- Topics are then sorted in decreasing order of these tuples to get the final order

### Stopwords
`data/stopwords/stopwords.txt` is a combination of three different kinds of stopwords:
- [SMART stopwords list](http://www.ai.mit.edu/projects/jmlr/papers/volume5/lewis04a/a11-smart-stop-list/)
- [English Personal Names](https://www.matthewjockers.net/macroanalysisbook/expanded-stopwords-list/)
- A [few archaic stopwords](data/stopwords/custom.txt) which were added manually 

## Examples
```
Input: bright key, white hair, green plain, weep, laughing, harm, happy, free, wind, wash, tongue, thousands
Output:
Come and see,
And let me not hurt
None of mine do harm;
I know that I am free.
And let me not,- I tell our children
Yet a thousand times
Dad I tell you, let me lie
Where ye are free,
As long as they should go
Sitting there in the road,
And I am learning to look
From my white hair:
And then I will be left by
Then weep that the wind's wake
Of my happiness is free;
And smile that it is
Long before yonder rose,
But never sleep, and never sleep
```

```
Input: frosty white, candy cane, jolly carols, celebration, gingerbread, mistletoe, snowflakes
Output:
Christmas blues clad in frosty white,
Sleigh bells falling from the mountaintop;
Christmas wreathed with gold and silver.
At midnight their winter carols are given out;
Chronicles of delight fall on christmas Eve!
Do you see me? Leave my little gingerbread house.
Do you hear those cheery roses?
Do not tell us what we might say:
Be that just as they sound like snowflakes
Nor make funful mistletoe
```

```
Input: dark woods, weeping river, full moon, freezing air, vengeance, sad
Output:
What do You Bless Me for
Ringing down in dark woods through freezing air,
Slowing sigh of your voice and sorrow;
Sweetness must perish thee in the dark woods.
Another half moon on the moon,
The sound of my blood rising out of the pale,
And the pain of revenge falling upon me?
Rich thanks you only for your song,
Then sing with me in this deep-engulf-time.
I have died of thy name
Till his blood no more.
He is too sad to suffer
The heart can not run across the seaside,
I am all but death in the weeping river.
I miss feeling the full moon,
The light fills my day,
The dark woods overshadowed by the still loss of vengeance
```

## References
- [Fine Tuning T5 for Summary Generation](https://github.com/abhimishra91/transformers-tutorials/blob/master/transformers_summarization_wandb.ipynb) 
- [T5 Finetuning Tips](https://discuss.huggingface.co/t/t5-finetuning-tips/684)
- [(Huggingface) T5 Docs](https://huggingface.co/transformers/model_doc/t5.html)
- [(Huggingface) Training T5](https://huggingface.co/transformers/model_doc/t5.html#training)
- [Finetuning T5 Tutorial](https://colab.research.google.com/github/patil-suraj/exploring-T5/blob/master/t5_fine_tuning.ipynb)
- [Few Shot Learning with T5](https://towardsdatascience.com/poor-mans-gpt-3-few-shot-text-generation-with-t5-transformer-51f1b01f843e)
- [Text Generation with Transformers](https://huggingface.co/blog/how-to-generate) 
