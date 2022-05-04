import pandas as pd
#ignore pandas warning
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class NLPImplicitAspectsClassifier:
	pos_words = None
	neg_words = None
	opinion_words = None

	def __init__(self):
		if NLPImplicitAspectsClassifier.opinion_words is None:
			# Load opinion lexicon
			neg_file = open("data/opinion-lexicon-English/negative_words.txt", encoding="ISO-8859-1")
			pos_file = open("data/opinion-lexicon-English/positive_words.txt", encoding="ISO-8859-1")
			NLPImplicitAspectsClassifier.pos_words = [line.strip() for line in pos_file.readlines()]
			NLPImplicitAspectsClassifier.neg_words = [line.strip() for line in neg_file.readlines()]
			NLPImplicitAspectsClassifier.opinion_words = NLPImplicitAspectsClassifier.pos_words + NLPImplicitAspectsClassifier.neg_words
		self.aspects_summary = pd.DataFrame(columns=["aspect", "sentiment", "score"])
		pass

	def feature_sentiment(self, sentence, token_id, aspect):
		senti_word = sentence[token_id]
		sentiment = 0
		if senti_word.text in NLPImplicitAspectsClassifier.opinion_words:
			sentiment = 1 if senti_word.text in NLPImplicitAspectsClassifier.pos_words else -1
			for child in senti_word.children:
				if child.dep_ == "neg":
					sentiment *= -1
				if child.dep_ == "admod" or child.dep_ == "advmod":
					sentiment *= 1.5
			
			self.aspects_summary = self.aspects_summary.append({
				'aspect': aspect, 
				'sentiment': 'positive' if sentiment>0 else 'negative',
				"score": sentiment
			}, ignore_index=True)
		
		return {"aspect": aspect, "sentiment": sentiment}