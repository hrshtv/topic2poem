from nltk import pos_tag
from nltk.tokenize import word_tokenize

class TopicExtractor:


    def __init__(self, path, punctuation):

        # Load the stopwords from a file
        with open(path, "r", encoding = "utf-8") as f:
            sw = f.readlines()
        sw = [w.strip() for w in sw[1:]] # Skip the first line
        sw += punctuation
        self.sw = sw

        # Initialize constants
        self.allowed_tags = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS", "VBG"]
        self.nouns = ["NN", "NNS", "NNP", "NNPS"]
        self.before_noun = ["JJ", "JJR", "JJS", "NN"]

        self.topics = None


    def extract(self, text):

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
                if len(topic) > 3:
                    unigrams.append(topic)

                # Bigrams
                if i > 1 and tag in self.nouns:

                    previous_tag = tagged[i-1][1]
                    previous_topic = tagged[i-1][0]

                    if previous_tag in self.before_noun:

                        bigrams.append(previous_topic + " " + topic)
                        unigrams_to_remove.append(topic)
                        unigrams_to_remove.append(previous_topic)

        topics = list(set(bigrams)) + list(set(unigrams) - set(unigrams_to_remove))

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
    The only other sound’s the sweep   
    Of easy wind and downy flake.   

    The woods are lovely, dark and deep,   
    But I have promises to keep,   
    And miles to go before I sleep,   
    And miles to go before I sleep.
    """

    from string import punctuation
    
    te = TopicExtractor("stopwords.txt", punctuation)
    topics = te.extract(text)
    print(topics)

