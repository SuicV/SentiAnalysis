import pandas as pd
from gensim.models import Word2Vec
from spacy.lang.en import English
import numpy as np
from tqdm import tqdm


class CoRefAspectIdentGrouping:
	"""
	class for co-referential aspects (aspects that have same meaning) identification and grouping.
		:model_wv word2vect model
	"""
	model_wv = None

	def __init__(self, reviews: pd.DataFrame, aspects_freq: dict, nlp: English):
		"""
		constructor of the class
		@param review DataFrame contains review and cleaned_review columns
		@param aspects_freq dictionary of aspect frequency
		@param nlp instance of English spacy object for NLP
		@return CoRefAspectIdentGrouping
		"""
		self.__reviews = reviews
		self.__aspects_freq = aspects_freq
		self.__aspects = list(dict(self.__aspects_freq).keys())
		self.__nlp = nlp

	def get_co_occurrence_matrix(self, senti_words_allowed_tags=["ADJ"]):
		"""
		method calculate the co-occurrence of extracted aspects and sentiment words. The sentiment words extracted using
		part of speech tag
		@param senti_words_allowed_tags:list allowed part of speech tag for extracting sentiment words
		@return aspect_sentiment:DataFrame co-occurrence matrix
		"""
		aspect_sentiment = pd.DataFrame(columns=self.__aspects)
		aspects_count = len(self.__aspects)
		for id_, review in self.__reviews["cleaned_review"].items():
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

	def __train_word2vec(self):
		"""
		method to word2vec model provided by gensim library. The model is trained on reviews words
		@return: Word2Vec trained model
		"""
		review_sentences = []
		for id_, review in tqdm(self.__reviews["review"].items()):
			doc = self.__nlp(review)
			sentences = []
			for sentence in doc.sents:
				sentence_words = []
				for word in sentence:
					if (not word.is_digit) and (not word.is_punct):
						word = word.lemma_.lower().replace("-", "")
						sentence_words.append(word)
				review_sentences.append(sentence_words)
		return Word2Vec(sentences=review_sentences, vector_size=300, window=5, min_count=5, workers=2, sg=1)

	def __merge_pairs(self, d, l, s=[]):
		"""
		method to merge pairs of similar aspects to construct groups
		@param d: list of pairs
		@param l: first pair to start with
		@param s: start list
		@return:
		"""
		if not (r := [i for i in d if any(j in l for j in i) and i not in s]):
			yield list(set(l))
			if (new_r := [i for i in d if i not in s]):
				yield from self.__merge_pairs(d, new_r[0], s=s + [new_r[0]])
		else:
			yield from self.__merge_pairs(d, l + [i for k in r for i in k], s=s + r)

	def get_co_reference_aspects_groups(self, threshold):
		"""
		method to get co-reference aspects groups. it's identify similar aspects using similarity threshold calculated
		based on word2vec model.

		@param threshold: threshold of merging two aspects
		@return: named_named_explicit_aspects dictionary of groups. The key is group name, and value is list of
			aspects of this group
		"""
		if self.model_wv == None:
			self.model_wv = self.__train_word2vec()
		# create pairs of similar aspects
		aspect_pairs_list = [set([i]) for i in set(self.__aspects)]
		for aspect in self.__aspects:
			for aspect2 in self.__aspects:
				if aspect != aspect2:
					similarity = self.model_wv.wv.similarity(aspect, aspect2)
					pair = {aspect, aspect2}
					if similarity > threshold and pair not in aspect_pairs_list:
						aspect_pairs_list.append(pair)

		# convert set type to list type.
		for i, aspect_pair in enumerate(aspect_pairs_list):
			aspect_pairs_list[i] = list(aspect_pair)

		# merging pairs to create groups
		aspects_groups = list(self.__merge_pairs(aspect_pairs_list, aspect_pairs_list[0]))

		# name groups based on maximum occurrence of an aspect in the group
		group_names = []
		for group in aspects_groups:
			max_of_group = ("", 0)
			for item in group:
				freq = self.__aspects_freq[item]
				if freq > max_of_group[1]:
					max_of_group = (item, freq)
			group_names.append(max_of_group[0])

		# map each aspect with the correct name group
		named_explicit_aspects = {}
		for i, group_name in enumerate(group_names):
			named_explicit_aspects[group_name] = aspects_groups[i]
		return named_explicit_aspects
