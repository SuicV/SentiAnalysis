from Scrappers.AgodaScrapper import AgodaScrapper
from Scrappers.TripAdvisorScrapper import TripAdvisorScrapper
from Scrappers.BookingScrapper import BookingScrapper
from time import time



tripadvisor_scraper = TripAdvisorScrapper()
hotels_link = tripadvisor_scraper.get_hotels("paris hotels")
print(len(hotels_link))
for hotel_link in hotels_link:
    print(hotel_link)

hotel_reviews = tripadvisor_scraper.get_reviews("https://www.tripadvisor.com/Hotel_Review-g187147-d228694-Reviews-Hotel_Malte_Astotel-Paris_Ile_de_France.html", 1)
print(hotel_reviews)

tripadvisor_scraper.scrapper.quit()


"""
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
"""