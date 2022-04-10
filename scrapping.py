from Scrappers.TripAdvisorScrapper import TripAdvisorScrapper

scrapper = TripAdvisorScrapper("data/reviews_paris_hotels_5.csv")

scrapper.start("Paris hotels", 2)