import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

class TripAdvisorScrapper:
	def __init__(self):
		conf_parser = configparser.ConfigParser()
		conf_parser.read(".env")
		self.scrapper = webdriver.Chrome(conf_parser["SELENIUM"]["DRIVER_PATH"])
		pass

	def get_hotels(self):
		self.scrapper.get("https://www.tripadvisor.com")
		# search
		els = self.scrapper.find_element(By.CSS_SELECTOR, "input[placeholder='Where to?']")
		els.send_keys("Morocco hotels")
		# submit request
		els.submit()
		# get listing items
		listings = self.scrapper.find_elements(By.CSS_SELECTOR, ".listItem")
		links =[]
		for listing in listings:
			title = listing.find_element(By.CSS_SELECTOR, ".listing_title a")
			links.append({"title": title.text, "link": title.get_dom_attribute("href")})

		pd.DataFrame(links).to_csv("./data/links.csv", header=True)

		self.scrapper.quit()
		pass

	def get_reviews(self, link):
		pass

	def start(self):
		# self.get_hotels()
		links = pd.read_csv('./data/links.csv', header=0)
		for id, row in links[["title", "link"]].iterrows():
			self.scrapper.get(f"https://www.tripadvisor.com{row['link']}#REVIEWS")
			break