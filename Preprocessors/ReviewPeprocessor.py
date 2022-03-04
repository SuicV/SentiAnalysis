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
		self.__reviews = self.__reviews.apply(lambda r: r.replace("\n", " ").replace("\t", " ").replace("\r", " "))
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
			words = re.findall("[\w']+", review)
			for word in words:
				correction = spell_checker.correction(word)
				review = review.replace(word, correction)
			self.__reviews[index] = review
		pass

	def start(self):
		"""
		run the preprocessing on reviews.

		:return: __reviews
		"""
		self.remove_tags()
		self.spelling_correction()

		return self.__reviews