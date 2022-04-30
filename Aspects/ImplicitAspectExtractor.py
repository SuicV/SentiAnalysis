import pandas as pd
from spacy.lang.en import English
from spacy.matcher import Matcher
from tqdm import tqdm


class ImplicitAspectExtractor:
	"""
	class for extracting implicit aspects. the implemented method is based on the algorithm proposed in this paper A Hybrid Co‑occurrence and Ranking‑based Approach for Detection
of Implicit Aspects in Aspect‑Based Sentiment Analysis (DIO: 10.1007/s42979-020-00138-7)
	the main idea is
	"""

	def __init__(self, reviews: pd.Series, co_occurrence_matrix: pd.DataFrame, nlp: English):
		"""
		constructor method
		@param reviews: cleaned reviews
		@param co_occurrence_matrix: co occurrence matrix (explicit aspects/sentiment word)
		@param nlp: spacy instant for NLP
		"""
		self.__nlp = nlp
		self.__reviews = reviews
		self.__explicit_aspects = co_occurrence_matrix.columns
		self.__co_occurrence_matrix = co_occurrence_matrix

	def extract_implicit_aspects(self):
		result = pd.DataFrame(columns=["review_id", "sentence", "implicit_aspects"])

		# crate pattern for spacy matcher
		pattern = [{"POS": "ADJ"}]
		matcher = Matcher(self.__nlp.vocab)
		matcher.add("SENTIMENT_WORDS", [pattern])

		sentiment_words = list(self.__co_occurrence_matrix.index)
		for id_, review in tqdm(self.__reviews.items()):
			doc = self.__nlp(review)
			for sentence in doc.sents:
				# get explicit aspects from sentence
				aspects_in_sentence = [i for i in self.__explicit_aspects if i in sentence.text]
				# opinionated sentence but it does not contain explicit aspect word
				if len(aspects_in_sentence) == 0:
					# extract ADJ
					extracted_ADJS = matcher(sentence)
					implicit_aspects = []
					for id_matcher, start, end in extracted_ADJS:
						sentiment_word = sentence[start:end].text
						if sentiment_word in sentiment_words:
							# get the highest co-occurred explicit aspect with sentiment word
							implicit_aspect = self.__co_occurrence_matrix.loc[sentiment_word].sort_values(ascending=False).index[0]
							implicit_aspects.append(implicit_aspect)
					# add implicit aspects and sentence to the result dataframe
					if len(implicit_aspects) > 0:
						result = result.append({
							"review_id": id_,
							"sentence": sentence.text,
							"implicit_aspects": implicit_aspects
						}, ignore_index=True)
		return result
