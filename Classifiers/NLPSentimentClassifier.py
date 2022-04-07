from collections import Counter
import os
import pandas as pd
from spacy.lang.en import English
from tqdm import tqdm
#ignore pandas warning
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class NLPSentimentClassifier:

	pos_words = None
	neg_words = None
	opinion_words = None

	def __init__(self, reviews: pd.Series, explicit_aspects: list, nlp: English):
		self.__nlp = nlp
		self.__reviews = reviews
		self.__explicit_aspects = explicit_aspects
		if NLPSentimentClassifier.opinion_words is None:
			# Load opinion lexicon
			neg_file = open("../data/opinion-lexicon-English/negative_words.txt", encoding="ISO-8859-1")
			pos_file = open("../data/opinion-lexicon-English/positive_words.txt", encoding="ISO-8859-1")
			NLPSentimentClassifier.pos_words = [line.strip() for line in pos_file.readlines()]
			NLPSentimentClassifier.neg_words = [line.strip() for line in neg_file.readlines()]
			NLPSentimentClassifier.opinion_words = NLPSentimentClassifier.pos_words + NLPSentimentClassifier.neg_words
		pass

	def feature_sentiment(self, sentence):
		'''
		input: dictionary and sentence
		function: appends dictionary with new features if the feature did not exist previously,
				  then updates sentiment to each of the new or existing features
		output: updated dictionary
		'''

		sent_dict = Counter()
		debug = 0
		for token in sentence:
			#    print(token.text,token.dep_, token.head, token.head.dep_)
			# check if the word is an opinion word, then assign sentiment
			if token.text in NLPSentimentClassifier.opinion_words:
				sentiment = 1 if token.text in NLPSentimentClassifier.pos_words else -1
				# if target is an adverb modifier (i.e. pretty, highly, etc.)
				# but happens to be an opinion word, ignore and pass
				if (token.dep_ == "advmod"):
					continue
				elif (token.dep_ == "amod"):

					for child in token.children:
						# if there's a adj modifier (i.e. very, pretty, etc.) add more weight to sentiment
						# This could be better updated for modifiers that either positively or negatively emphasize
						if ((child.dep_ == "amod") or (child.dep_ == "advmod")):
							sentiment *= 1.5
						# check for negation words and flip the sign of sentiment
						if child.dep_ == "neg":
							sentiment *= -1

					sent_dict[token.head.lemma_.lower()] += sentiment
				# for opinion words that are adjectives, adverbs, verbs...
				else:
					for child in token.children:
						# if there's a adj modifier (i.e. very, pretty, etc.) add more weight to sentiment
						# This could be better updated for modifiers that either positively or negatively emphasize
						if ((child.dep_ == "amod") or (child.dep_ == "advmod")):
							sentiment *= 1.5
						# check for negation words and flip the sign of sentiment
						if child.dep_ == "neg":
							sentiment *= -1
					for child in token.children:
						# if verb, check if there's a direct object
						if (token.pos_ == "VERB") & (child.dep_ == "dobj"):
							sent_dict[child.lemma_.lower()] += sentiment
							# check for conjugates (a AND b), then add both to dictionary
							subchildren = []
							conj = 0
							for subchild in child.children:
								if subchild.text == "and":
									conj = 1
								if (conj == 1) and (subchild.text != "and"):
									subchildren.append(subchild.lemma_.lower())
									conj = 0
							for subchild in subchildren:
								sent_dict[subchild] += sentiment

					# check for negation
					for child in token.head.children:
						if ((child.dep_ == "amod") or (child.dep_ == "advmod")):
							sentiment *= 1.5
						# check for negation words and flip the sign of sentiment
						if (child.dep_ == "neg"):
							sentiment *= -1

					# check for nouns
					for child in token.head.children:
						noun = ""
						if (child.pos_ == "NOUN") and (child.text not in sent_dict):
							noun = child.lemma_.lower()
							# Check for compound nouns
							for subchild in child.children:
								if subchild.dep_ == "compound":
									noun = subchild.lemma_.lower() + " " + noun
							sent_dict[noun] += sentiment
						debug += 1
		return sent_dict

	def extract_sentiment_aspect(self, review):
		sentences = self.__nlp(review).sents
		res = []
		for sentence in sentences:
			f = self.feature_sentiment(sentence)
			# don't add empty objects
			if f != {}:
				res.append(f)
		return res

	def start(self):
		result = self.__reviews.apply(lambda review: self.extract_sentiment_aspect(review))
		aspects_summary = pd.DataFrame(columns=["aspect", "sentiment", "score"])
		for id_, items in tqdm(result.items()):
			to_append = []
			for item in items:
				for i in item:
					if i in self.__explicit_aspects:
						to_add = pd.Series([i, "positive" if item[i] > 0 else "negative", item[i]],
						                   index=["aspect", "sentiment", "score"])
						aspects_summary = aspects_summary.append(to_add, ignore_index=True)
		groped_aspects_summary = aspects_summary.groupby(["aspect", "sentiment"]).size().reset_index(
			name="count").sort_values("count", ascending=False)
		return groped_aspects_summary
	pass
