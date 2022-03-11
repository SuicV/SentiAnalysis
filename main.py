from Preprocessors.ReviewPreprocessor import ReviewPreprocessor
import pandas as pd
import spacy
from Aspects.ExplicitAspectExtractor import ExplicitAspectExtractor

from time import time

now = time()
data = pd.read_csv("data/reviews_paris_hotels.csv")
preprocessor = ReviewPreprocessor(data["review"])
data["cleaned_reviews"] = preprocessor.start()
print(f"preprocessing in : {time() - now}s")

now = time()
nlp = spacy.load("en_core_web_sm")
print(f"loading en_core_web_sm {time() - now}s")

now = time()
aspect_extractor = ExplicitAspectExtractor(data["cleaned_reviews"], nlp)
aspects = aspect_extractor.start(50)
print(aspects)
print(f"extracting aspects {time() - now}s")

