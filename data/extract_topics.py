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
            pos = scores_dict["pos"]
            neg = scores_dict["neg"]
            neu = scores_dict["neu"]
            if stype == "neu":
                temp = sorted([pos, neg], reverse = True)
                temp = tuple([0, sval] + temp)
                topic_scores.append(temp)
            else:
                if stype == "pos":
                    topic_scores.append((1, sval, neg))
                else:
                    topic_scores.append((1, sval, pos))
        
        # Sort by topic scores
        ranked_topics = [t for _, t in sorted(zip(topic_scores, topics), reverse = True)]
        
        # for s, t in sorted(zip(topic_scores, topics), reverse = True):
        #     print(s, " | ", t)

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
        Not only that, the year will come when you will wake up in the middle of the night and realize that the people you went to school with are in positions of power, and may soon actually be running things. If there’s anything more calculated to thick men’s blood with cold, it’s that. After all, you know how much they didn’t know then, and, given yourself as an example, you can’t assume they know a great deal more now. “We’re all doomed,” you will think. (For example: Brian Mulroney is only a year older than I am.) You may feel that the only thing to do when you’ve reached this stage is to take up nail-biting, mantras, or jogging, all of which would be recognized by animal behavior specialists as substitution activities, like scratching, which are resorted to in moments of unresolved conflict. But we’ll get around to some positive thinking in a moment.

What shall I tell them! I thought, breaking out into a cold sweat, as I tossed and turned night after night. (Lest you leap to indulge in Calvinistic guilt at the idea of having been the proximate cause of my discomfort, let me hasten to add that I was on a boat. The tossing and turning was par for the course, and the cold sweat can be cured by Gravol). For a while I toyed with the idea of paraphrasing Kurt Vonnegut, who told one graduating class, “Everything is going to become unbelievably worse and will never get better again,” and walked off the stage. But that’s the American style: boom or bust. A Canadian would be more apt to say, “things may be pretty mediocre but let’s at least try to hold the line.”

Then I thought that maybe I could say a few words on the subject of a liberal arts education, and how it prepares you for life. But sober reflection led me to the conclusion that this topic too was a washout; for, as you will soon discover, a liberal arts education doesn’t exactly prepare you for life. A preparation-for-life curriculum would not consist of courses on Victorian Thought and French Romanticism, but of things like How to Cope With Marital Breakdown, Getting More for your Footwear Dollar, Dealing With Stress, and How To Keep Your Fingernails from Breaking Off by Always Filing Them Towards the Center; in other words, it would read like the contents page of Homemakers Magazine, which is why Homemakers Magazine is so widely read, even by me. Or, for boys, Forbes or The Economist , and Improving Your Place in the Power Hierarchy by Choosing the Right Suit. (Dark blue with a faint white pinstripe, not too far apart, in case you’re interested.)

Or maybe, I thought, I should expose glaring errors in the educational system, or compile a list of things I was taught which are palpably not true. For instance, in high school I made the mistake of taking Home Economics instead of Typing - we thought, in those days, that if you took the commercial course most of your eyebrows would come off and would have to be drawn on with a pencil for the rest of your life - where I was told that every meal should consist of a brown thing, a white thing, a yellow thing and a green thing; that it was not right to lick the spoon while cooking; and that the inside of a dress seam was as important as the outside. All three of these ideas are false and should be discarded immediately by anyone who still holds them.

Nor did anyone have the foresight to inform me that the best thing I could do for myself as a writer would be back and wrist exercises. No one has yet done a study of this, but they will, and when they start excavating and measuring the spines and arm bones of the skeletons of famous writers of the past I am sure they will find that those who wrote the longest novels, such as Dickens and Melville, also had the thickest wrists. The real reason that Emily Dickinson stuck to lyric poems with relatively few stanzas is that she had spindly fingers. You may scoff, but future research will prove me right.

But I then thought, I shouldn’t talk about writing. Few of this graduating class will wish to be writers, and those that do should by no means be encouraged. Weave a circle round them thrice, and close your eyes holy dread, because who needs the competition? What with the proliferation of Creative Writing courses, a mushroom of recent growth all but unknown in my youth, we will soon have a state of affairs in which everybody writes and nobody reads, the exact reverse of the way things were when I was composing dolorous verses in a rented cupboard on Charles Street in the early sixties.

Or maybe, I thought, I should relate to them a little known fact of shocking import, which they will remember vividly when they have all but forgotten the rest of this speech. For example: nobody ever tells you, but did you know that when you have a baby your hair falls out? Not all of it, and not all at once, but it does fall out. It has something to do with a zinc imbalance. The good news is that it does grow back in. This only applies to girls. With boys, it falls out whether you have a baby or not, and it never grows back in; but even then there is hope. In a pinch, you can resort to quotation, a commodity which a liberal arts education teaches you to treat with respect, and I offer the following: “God only made a few perfect heads, and the rest lie covered with hair.”

Which illustrates the following point: when faced with the inevitable, you always have a choice. You may not be able to alter reality, but you can alter your attitude towards it. As I learned during my liberal arts education, any symbol can have, in the imaginative context, two versions, a positive and a negative. Blood can either be the gift of life or what comes out of you when you cut your wrists in the bathtub. Or, somewhat less drastically, if you spill your milk you’re left with a glass which is either half empty or half full.

Which brings us to the hidden agenda of this speech. What you are being ejected into today is a world that is both half empty and half full. On the one hand, the biosphere is rotting away. The raindrops that keep falling on your head are also killing the fish, the trees, the animals, and, if they keep being as acid as they are now, they’ll eventually do away with things a lot closer to home, such as crops, front lawns and your digestive tract. Nature is no longer what surrounds us, we surround it, and the switch has not been for the better. On the other hand, unlike the ancient Egyptians, we as a civilization know what mistakes we are making and we also have the technology to stop making them; all that is lacking is the will.

Another example: on the one hand, we ourselves live daily with the threat of annihilation. We’re just a computer button and a few minutes away from it, and the gap between us and it is narrowing every day. We secretly think in terms not of “If the Bomb Drops” but of “When the Bomb Drops”, and it’s understandable if we sometimes let ourselves slide into a mental state of powerlessness and consequent apathy. On the other hand, the catastrophe that threatens us as a species, and most other species as well, is not unpredictable and uncontrollable, like the eruption of the volcano that destroyed Pompeii. If it occurs, we can die with the dubious satisfaction of knowing that the death of the world was a man-made and therefore preventable event, and that the failure to prevent it was a failure of human will.

This is the kind of world we find ourselves in, and it’s not pleasant. Faced with facts this depressing, the question of the economy - or how many of us in this country can afford two cars doesn’t really loom too large, but you’d never know it from reading the papers. Things are in fact a lot worse elsewhere, where expectations center not on cars and houses and jobs but on the next elusive meal. That’s part of the down side. The up side, here and now, is that this is still more or less a democracy; you don’t get shot or tortured yet for expressing an opinion, and politicians, motivated as they may be by greed and the lust for power, are nevertheless or because of this, still swayed by public opinion. The issues raised in any election are issues perceived by those who want power to be of importance to those in a position to confer it upon them. In other words, if enough people show by the issues they raise and by the way they’re willing to vote that they want changes made, then change becomes possible. You may not be able to alter reality, but you can alter your attitude towards it, and this, paradoxically, alters reality.
    """

    from string import punctuation
    
    te = TopicExtractor("stopwords/stopwords.txt", punctuation)
    topics = te.extract(text, seed = 0)
    print(topics)

