from collections import Counter

from pandas import Series
from spacy.lang.en import English


class ExplicitAspectExtractor:
	__aspects = {}

	def __init__(self, reviews: Series, nlp: English):
		self.__reviews = reviews
		self.__nlp = nlp

	def extract_aspects(self):
		for index, review in self.__reviews.items():
			doc = self.__nlp(review)
			for token in doc:
				if token.pos_ == "NOUN" and not token.is_stop and not token.is_punct:
					if token.text.lower() in self.__aspects.keys():
						self.__aspects[token.text.lower()] += 1
					else:
						self.__aspects[token.text] = 1
				pass
		pass

	def get_frequent_aspects(self, threshold: int):
		return Counter(self.__aspects).most_common(threshold)

	def start(self, threshold):
		self.extract_aspects()
		return self.get_frequent_aspects(threshold)
