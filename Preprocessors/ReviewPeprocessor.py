import nltk
from nltk.tokenize import sent_tokenize
from textblob import TextBlob
from spellchecker import SpellChecker

from pandas import Series

import re


class ReviewPreprocessor:
	"""
	class ReviewPreprocessor
		class for preprocessing reviews.
	"""

	def __init__(self, reviews: Series):
		"""
		construction method, it assign reviews param to __reviews attribute.

		:param reviews: reviews to preprocess
		"""
		self.__reviews = reviews

	def remove_tags(self):
		"""
		remove useless feature from reviews.

		:return: None
		"""
		# remove \r \n \t tags
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"\\n", " ", r))
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"\\r", " ", r))
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"\\t", " ", r))
		# remove # tags
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"#\S+", "", r, flags=re.IGNORECASE))
		# remove @ tags
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"@\S+", "", r, flags=re.IGNORECASE))
		# remove links
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"(http(s)?:/|www)\S+", "", r, flags=re.IGNORECASE))
		pass

	def spelling_correction(self):
		"""
		correct misspelling words from reviews. this methode use SpellChecker package.
		check documentation of SpellChecker in this link https://pyspellchecker.readthedocs.io/en/latest/

		:return: None
		"""
		spell_checker = SpellChecker()
		for index, review in self.__reviews.items():
			words = re.findall("[\w'’]+", review)
			for word in words:
				correction = spell_checker.correction(word)
				review = review.replace(word, correction)
			self.__reviews[index] = review
		pass

	def remove_objective_sentences(self):
		"""
		methode to remove objective sentences from reviews.

		:return:
		"""
		for index, review in self.__reviews.items():
			sentences = sent_tokenize(review)

			for index_s, sentence in enumerate(sentences):
				subjective_score = TextBlob(sentence).subjectivity
				if subjective_score < 0.4:
					del sentences[index_s]

			self.__reviews[index] = " ".join(sentences)

	def start(self):
		"""
		run the preprocessing on reviews.

		:return: __reviews
		"""
		self.remove_tags()
		self.spelling_correction()
		self.remove_objective_sentences()
		return self.__reviews
