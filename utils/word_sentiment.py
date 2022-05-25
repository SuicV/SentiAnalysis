from nltk.corpus import sentiwordnet as snw
from statistics import mean


def __get_wordnet_pos(tag):
    if tag == "ADJ":
        return "a"
    elif tag == "NOUN":
        return "n"
    elif tag == "ADV":
        return "r"
    elif tag == "VERB":
        return 'v'
    return None

def word_sentiment(word, POS, threshold = 0.2):
    wn_pos = __get_wordnet_pos(POS)
    if wn_pos :
        synsets = snw.senti_synsets(word, wn_pos)

        neg_scores = []
        pos_scores = []

        for synset in synsets:
            neg_scores.append(synset.neg_score())
            pos_scores.append(synset.pos_score())

        neg_score = max(neg_scores) if len(neg_scores) > 0 else 0
        pos_score = max(pos_scores) if len(pos_scores) > 0 else 0

        if pos_score > neg_score and pos_score >= threshold:
            return 1
        elif neg_score > pos_score and neg_score >= threshold:
            return -1
    return 0
