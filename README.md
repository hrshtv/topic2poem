# text2poem
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
- Using [VADER](https://www.nltk.org/_modules/nltk/sentiment/vader.html), each topic's sentiment (`pos, neg, neu`) scores are obtained. 
- Positive and negative topics have equal preference and are preferred over neutral topics 
- Topics are then sorted in decreasing order of their sentiment scores to obtain the final order

## References
- [Fine Tuning T5 for Summary Generation](https://github.com/abhimishra91/transformers-tutorials/blob/master/transformers_summarization_wandb.ipynb) 
- [T5 Finetuning Tips](https://discuss.huggingface.co/t/t5-finetuning-tips/684)
- [(Huggingface) T5 Docs](https://huggingface.co/transformers/model_doc/t5.html)
- [(Huggingface) Training T5](https://huggingface.co/transformers/model_doc/t5.html#training)
- [Finetuning T5 Tutorial](https://colab.research.google.com/github/patil-suraj/exploring-T5/blob/master/t5_fine_tuning.ipynb)
- [Few Shot Learning with T5](https://towardsdatascience.com/poor-mans-gpt-3-few-shot-text-generation-with-t5-transformer-51f1b01f843e)
- [Text Generation with Transformers](https://huggingface.co/blog/how-to-generate) 
