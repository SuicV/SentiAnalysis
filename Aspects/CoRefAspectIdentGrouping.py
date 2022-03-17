import pandas as pd
from spacy.lang.en import English
import numpy as np


class CoRefAspectIdentGrouping:
	def __init__(self, reviews: pd.Series, aspects: list, nlp: English):
		self.__reviews = reviews
		self.__aspects = aspects
		self.__nlp = nlp

	def get_co_occurrence_matrix(self, senti_words_allowed_tags):
		aspect_sentiment = pd.DataFrame(columns=self.__aspects)
		aspects_count = len(self.__aspects)
		for id_, review in self.__reviews.items():
			doc = self.__nlp(review)
			for sentence in doc.sents:
				aspects = []
				sentiment_words = []
				for word in sentence:
					if word.pos_ == "NOUN" and word.lemma_ in self.__aspects and word.lemma_ not in aspects:
						aspects.append(word.lemma_)
					if word.pos_ in senti_words_allowed_tags:
						sentiment_words.append(word.lemma_)
				if aspects != [] and sentiment_words != []:
					for senti_word in sentiment_words:
						if senti_word not in aspect_sentiment.index:
							s = pd.DataFrame(np.zeros(aspects_count).reshape(1, aspects_count), columns=self.__aspects,
							                 index=[senti_word])
							s.loc[:, aspects] = 1.0
							aspect_sentiment = pd.concat([aspect_sentiment, s])
						else:
							aspect_sentiment.loc[senti_word, aspects] += 1
		return aspect_sentiment
