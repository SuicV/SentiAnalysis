import configparser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd

class TripAdvisorScrapper:
	def __init__(self, output):
		conf_parser = configparser.ConfigParser()
		conf_parser.read(".env")
		self.scrapper = webdriver.Chrome(conf_parser["SELENIUM"]["DRIVER_PATH"])
		self.output = output
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
			links.append({"title": title.text, "link": "https://www.tripadvisor.com"+title.get_dom_attribute("href")})

		pd.DataFrame(links).to_csv("./data/links.csv", header=True)

	def get_reviews(self, link):
		reviews = []

		self.scrapper.get(f"{link}#REVIEWS")
		listing_title = self.scrapper.find_element(By.CSS_SELECTOR, "#HEADING").text
		listing_rating = self.scrapper.find_element(By.CSS_SELECTOR, "span.P").text
		reviews_els = self.scrapper.find_elements(By.CSS_SELECTOR, "div[data-test-target='HR_CC_CARD']")

		for review in reviews_els:
			# get opinion holder
			review_holder = review.find_element(By.CSS_SELECTOR, ".ui_header_link").text

			# get rating
			rating = review.find_element(By.CSS_SELECTOR, "div[data-test-target='review-rating'] span")
			rating = rating.get_attribute("class")[-2:]
			review_rating = rating[0]+"."+rating[1]

			# get review title
			review_title = review.find_element(By.CSS_SELECTOR, "div[data-test-target='review-title']")
			review_title_str = review_title.text
			# click to show the rest of comment
			review_title.find_element(By.TAG_NAME, "a").click()

			# get review
			review_str = review.find_element(By.CSS_SELECTOR, "div._T q._a").text
			reviews.append({
				'listing_name': listing_title, 'listing_score': listing_rating, 'username': review_holder,
				'review_score': review_rating, 'review_title': review_title_str, 'review': review_str
			})

		return reviews

	def start(self):
		# self.get_hotels()
		links = pd.read_csv('./data/links.csv', header=0)
		reviews_df = pd.DataFrame(columns = ['listing_name', 'listing_score', 'username', 'review_score', 'review_title', 'review'])

		for id, link in links["link"].items():
			try :
				reviews_dict = self.get_reviews(link)
				reviews_df = reviews_df.append(reviews_dict, ignore_index=True, sort=False)
			except NoSuchElementException as e:
				print("NoSuchElementException error")

		self.scrapper.quit()
		reviews_df.to_csv(self.output, header=True, index = False)