"""
    Description: Extracts topics (bigrams and unigrams) from given text using POS-Tagging and rank them using sentiment intensity
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
        diff = [item for item in l1 if item not in l2]
        return diff


    def rank(self, topics):
        topic_scores = []
        for t in topics:
            scores_dict = self.sia.polarity_scores(t) # reference: http://www.nltk.org/howto/sentiment.html
            del scores_dict["compound"]
            stype = max(scores_dict, key = scores_dict.get)
            sval = scores_dict[stype]
            if stype == "neu":
                topic_scores.append((0, sval))
            else:
                topic_scores.append((1, sval))
        # Sort by topic scores
        ranked_topics = [t for _, t in sorted(zip(topic_scores, topics), reverse = True)]
        return ranked_topics


    def extract(self, text, seed = None, random_rank = False):

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

            if (topic.lower() not in self.sw) and (tag in self.allowed_tags):

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
        Risest thou thus, dim dawn, again,
        And howlest, issuing out of night,
        With blasts that blow the poplar white,
        And lash with storm the streaming pane?

        Day, when my crowned estate begun
        To pine in that reverse of doom,
        Which sickened every living bloom,
        And blurred the splendour of the sun;

        Who usherest in the dolorous hour
        With thy quick tears that make the rose
        Pull sideways, and the daisy close
        Her crimson fringes to the shower;

        Who might'st have heaved a windless flame
        Up the deep East, or, whispering, played
        A chequer-work of beam and shade
        Along the hills, yet looked the same.

        As wan, as chill, as wild as now;
        Day, marked as with some hideous crime,
        When the dark hand struck down thro' time,
        And cancelled nature's best: but thou,

        Lift as thou may'st thy burthened brows
        Thro' clouds that drench the morning star,
        And whirl the ungarnered sheaf afar,
        And sow the sky with flying boughs,

        And up thy vault with roaring sound
        Climb thy thick noon, disastrous day;
        Touch thy dull goal of joyless gray,
        And hide thy shame beneath the ground
    """

    from string import punctuation
    
    te = TopicExtractor("stopwords/stopwords.txt", punctuation)
    topics = te.extract(text, seed = 0)
    print(topics)

