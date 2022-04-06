from nltk.tokenize import sent_tokenize
from nltk.tokenize import WhitespaceTokenizer
from spacy.lang.en import English
from textblob import TextBlob
from spellchecker import SpellChecker
from tqdm import tqdm
from pandas import Series

import re


class ReviewPreprocessor:
	"""
	class ReviewPreprocessor
		class for preprocessing reviews.
	"""

	def __init__(self, reviews: Series, nlp:English, spell_allowed_words=[], subjectivity_threshold = 0.4):
		"""
		construction method, it assign reviews param to __reviews attribute.

		:param reviews: reviews to preprocess
		"""
		self.__reviews = reviews
		self.spell_allowed_words = spell_allowed_words
		self.subjectivity_threshold = subjectivity_threshold
		self.__nlp = nlp

	def remove_tags(self):
		"""
		remove useless feature from reviews.

		:return: None
		"""
		# remove \r \n \t tags
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"\n", " ", r))
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"\r", " ", r))
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"\t", " ", r))
		# remove # tags
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"#\S+", " ", r, flags=re.IGNORECASE))
		# remove @ tags
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"@\S+", " ", r, flags=re.IGNORECASE))
		# remove links
		self.__reviews = self.__reviews.apply(lambda r: re.sub(r"(http(s)?:/|www)\S+", " ", r, flags=re.IGNORECASE))
		# remove emojis
		emoji_pattern = re.compile("["
		                           u"\U0001F600-\U0001F64F"  # emoticons
		                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
		                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
		                           u"\U00002500-\U00002BEF"  # chinese char
		                           u"\U00002702-\U000027B0"
		                           u"\U00002702-\U000027B0"
		                           u"\U000024C2-\U0001F251"
		                           u"\U0001f926-\U0001f937"
		                           u"\U00010000-\U0010ffff"
		                           u"\u2640-\u2642"
		                           u"\u2600-\u2B55"
		                           u"\u200d"
		                           u"\u23cf"
		                           u"\u23e9"
		                           u"\u231a"
		                           u"\ufe0f"  # dingbats
		                           u"\u3030"
		                           "]+", flags=re.UNICODE)
		self.__reviews = self.__reviews.apply(lambda r: emoji_pattern.sub(r'', r))
		return self.__reviews

	def spelling_correction(self):
		"""
		correct misspelled words from reviews. this methode use SpellChecker package.
		check documentation of SpellChecker in this link https://pyspellchecker.readthedocs.io/en/latest/

		:return: None
		"""
		spell_checker = SpellChecker()
		spell_checker.word_frequency.load_words(self.spell_allowed_words)
		for index, review in tqdm(self.__reviews.items()):
			words = re.findall(r"[\w'’]+", review)
			for word in words:
				if len(word) >= 2:
					correction = spell_checker.correction(word)
					review = review.replace(word, correction)
			self.__reviews[index] = review
		return self.__reviews

	def remove_objective_sentences(self):
		"""
		methode to remove objective sentences from reviews.

		:return:
		"""
		for index, review in tqdm(self.__reviews.items()):
			result = ""
			for sentence in list(self.__nlp(review).sents):
				sentence = sentence.text
				subjective_score = TextBlob(sentence).subjectivity
				if subjective_score >= self.subjectivity_threshold:
					result += " " + sentence

			self.__reviews.loc[index] = result
		return self.__reviews

	def start(self):
		"""
		run the preprocessing on reviews.

		:return: __reviews
		"""
		self.remove_tags()
		print("remove_tags done")
		self.spelling_correction()
		print("spelling_correction done")
		self.remove_objective_sentences()
		print("remove_objective_sentences done")
		return self.__reviews
