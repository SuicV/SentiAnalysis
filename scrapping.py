from logging import exception
from Scrappers.BookingScrapper import BookingScrapper
from Scrappers.TripAdvisorScrapper import TripAdvisorScrapper
import pandas as pd
from time import time


reviews = pd.DataFrame(columns=["listing_name", "listing_score", "username", "review_score", "review_title", "review"])
booking_scrapper = BookingScrapper()
reviews = booking_scrapper.get_reviews("https://www.booking.com/hotel/ma/riad-abaka.en-gb.html", 3)
booking_scrapper.scrapper.quit()
print(reviews)

trip_advisor_timing = time()
tripadvisor_scrapper = TripAdvisorScrapper()
hotels_links = pd.DataFrame(tripadvisor_scrapper.get_hotels("marrakech hotels"))
hotels_links.to_csv("./data/tripadvisor_links.csv", header=True, index=True)

reviews = pd.DataFrame(columns=["listing_name", "listing_score", "username", "review_score", "review_title", "review"])
for id_, row in hotels_links[0:5].iterrows():
    temp_reviews = tripadvisor_scrapper.get_reviews(row["link"], 3)
    if temp_reviews != False:
        pd.DataFrame(temp_reviews)
        temp_reviews["listing_name"] = row["listing_name"]
        temp_reviews["listing_score"] = row["listing_score"]
        reviews = pd.concat([reviews, temp_reviews], ignore_index=True, axis=0)
end_trip_advisor_timing = time()

tripadvisor_scrapper.scrapper.quit()

booking_timing = time()
booking_scrapper = BookingScrapper()
hotels_links = pd.DataFrame(booking_scrapper.get_hotels("marrakech hotels"))
hotels_links.to_csv("./data/booking_links.csv", header=True, index=True)

for id_, row in hotels_links[0:5].iterrows():
    temp_reviews = booking_scrapper.get_reviews(row["link"], 3)
    if temp_reviews != False :
        temp_reviews = pd.DataFrame(temp_reviews)
        temp_reviews["listing_name"] = row["listing_name"]
        temp_reviews["listing_score"] = row["listing_score"]
        reviews = pd.concat([reviews, temp_reviews], ignore_index=True, axis=0)
end_booking_timing = time()

booking_scrapper.scrapper.quit()

reviews.to_csv("./data/tripadvisor_booking_reviews_new.csv",header=True, index=True)
print("\n")
print(f"trip_advisor timing : {end_trip_advisor_timing - trip_advisor_timing}")
print(f"booking timing : {end_booking_timing - booking_timing}")
print(f"total timing : {end_booking_timing - trip_advisor_timing}")