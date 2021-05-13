"""
    Description: Extracts topics (bigrams and unigrams) from given text using POS-Tagging and rank them using VADER
    Author: Harshit Varma
"""

import random
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

    
class TopicExtractor:

    def __init__(self, path, punctuation):

        # Load the stopwords from a file
        with open(path, "r", encoding = "utf-8") as f:
            sw = f.readlines()
        sw = [w.strip() for w in sw[1:]] # Skip the first line
        sw += [p for p in punctuation]
        self.sw = sw

        self.punctuation = punctuation

        # Initialize constants
        self.allowed_tags = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS", "VBG"]
        self.nouns = ["NN", "NNS", "NNP", "NNPS"]
        self.before_noun = ["JJ", "JJR", "JJS", "NN"]

        self.topics = None

        self.sia = SentimentIntensityAnalyzer()


    def listDiff(self, l1, l2):
        """ Subtracts list 2 from list 1 """
        diff = [item for item in l1 if item not in l2]
        return diff


    def rank(self, topics):
        """ Scores and ranks the topics """

        topic_scores = []

        for t in topics:

            scores_dict = self.sia.polarity_scores(t) # reference: http://www.nltk.org/howto/sentiment.html
            del scores_dict["compound"]

            pos = scores_dict["pos"]
            neg = scores_dict["neg"]
            neu = scores_dict["neu"]

            stype = max(scores_dict, key = scores_dict.get)
            sval = scores_dict[stype]

            if stype == "neu":
                temp = [0, sval] + sorted([pos, neg], reverse = True)
                temp = tuple(temp)
                topic_scores.append(temp)
            else:
                if stype == "pos":
                    topic_scores.append((1, sval, neg))
                else:
                    topic_scores.append((1, sval, pos))
        
        # Sort by topic scores
        ranked_topics = [t for _, t in sorted(zip(topic_scores, topics), reverse = True)]
        
        return ranked_topics


    def extract(self, text, seed = None, random_rank = False):
        """ Extracts the list of ranked topics from the given text  """

        # To prevent bigrams moving to the next line
        text = text.replace("\n", " | ")

        text = text.lower() # truecasing may be a better solution

        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)

        unigrams = []
        bigrams  = []
        unigrams_to_remove = []

        for i in range(len(tagged)):

            topic = tagged[i][0]
            tag   = tagged[i][1]

            if (tag in self.allowed_tags) and (topic.lower() not in self.sw):

                # Unigrams
                if len(topic) > 3 and topic not in unigrams:
                        unigrams.append(topic)

                # Bigrams
                if i > 1 and tag in self.nouns:

                    previous_tag = tagged[i-1][1]
                    previous_topic = tagged[i-1][0]

                    if previous_tag in self.before_noun and previous_topic.lower() not in self.sw and len(previous_topic) > 3:

                        bigram = previous_topic + " " + topic

                        if bigram not in bigrams:
                            bigrams.append(bigram)

                        if topic not in unigrams_to_remove:
                            unigrams_to_remove.append(topic)

                        if previous_topic not in unigrams_to_remove:
                            unigrams_to_remove.append(previous_topic)

        unigrams = self.listDiff(unigrams, unigrams_to_remove)

        # Clean topics:
        bigrams = [b.strip(self.punctuation) for b in bigrams]
        unigrams = [u.strip(self.punctuation) for u in unigrams]

        # Rank topics:

        if random_rank:
            if seed is not None:
                random.Random(seed).shuffle(bigrams)
                random.Random(seed).shuffle(unigrams)
            else:
                random.shuffle(bigrams)
                random.shuffle(unigrams)
            topics = bigrams + unigrams

        else:
            topics = self.rank(bigrams) + self.rank(unigrams)
        
        self.topics = topics

        return topics


if __name__ == '__main__':

    text = """
        Whose woods these are I think I know.   
        His house is in the village though;   
        He will not see me stopping here   
        To watch his woods fill up with snow.   

        My little horse must think it queer   
        To stop without a farmhouse near   
        Between the woods and frozen lake   
        The darkest evening of the year.   

        He gives his harness bells a shake   
        To ask if there is some mistake.   
        The only other sound's the sweep   
        Of easy wind and downy flake.   

        The woods are lovely, dark and deep,   
        But I have promises to keep,   
        And miles to go before I sleep,   
        And miles to go before I sleep.
    """

    from string import punctuation
    
    te = TopicExtractor("stopwords/stopwords.txt", punctuation)
    topics = te.extract(text, seed = 0)
    print(topics)

