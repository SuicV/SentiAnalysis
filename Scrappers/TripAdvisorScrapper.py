import configparser
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class TripAdvisorScrapper:
	"""
	class to scrap reviewes from TripAdvisor.com
	"""
	def __init__(self):
		conf_parser = configparser.ConfigParser()
		conf_parser.read(".env")
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument("--disable-gpu")
		chrome_options.add_argument("--headless")
		self.scrapper = webdriver.Chrome(conf_parser["SELENIUM"]["DRIVER_PATH"], options=chrome_options)
		self.scrapper.implicitly_wait(10)
		pass

	def get_hotels(self, search_tag: str) -> list:
		"""
		method to get list of hotels by a search tag.
		Example "Paris Hotels" will return a list of hotels in Paris
		
		:param search_tag: query to search in tripadvisor landing page form

		:return list of dicts contains the following keys {'listing_name', 'listing_score', 'link'} or
			False if there is an Exception
		"""
		
		links = []
		self.scrapper.get("https://www.tripadvisor.com")
		try:
			# search
			els = self.scrapper.find_element(By.CSS_SELECTOR, "input[placeholder='Where to?']")
			els.send_keys(search_tag)
			# submit request
			els.submit()
			
			if "search?q=" in self.scrapper.current_url:
				print("invalid search")
				return False
			
			sleep(0.9)
			# get listing items
			listings = self.scrapper.find_elements(By.CSS_SELECTOR, ".listItem")
			
			for listing in listings:
				listing_name = listing.find_element(By.CSS_SELECTOR, ".listing_title a")
				listing_score = listing.find_element(By.CSS_SELECTOR, ".ui_bubble_rating").get_dom_attribute("alt").split(" ")[0]

				links.append({"listing_name": listing_name.text.strip(), "listing_score":listing_score, 
					"link": "https://www.tripadvisor.com" + listing_name.get_dom_attribute("href")})

		except Exception as e:
			print(e.__traceback__,"\n",e)
			return False
		return links

	def get_reviews(self, link: str, num_pages: int) -> list:
		"""
		scraps reviews in hotel link. this method goes through rating scores (5,4,2,1) and scrap review from
		each page at this rating score. 

		:param link hotel link
		:param num_pages maximum number of pages to scrap

		:return links array of dicts {"listing_name", "listing_score", "username", "review_score", "review_title", "review"}
		"""
		reviews = []
		print(link)
		self.scrapper.get(f"{link}#REVIEWS")
		sleep(1)
		try:
			# get hotel name
			listing_name = self.scrapper.find_element(By.ID, "HEADING").text
			
			# get hotel score
			listing_score = self.scrapper.find_element(By.CSS_SELECTOR, 
				'div[data-test-target="hr-aft-info"] span[class^="ui_bubble_rating bubble"').get_attribute("class")[-2:]
			listing_score = f"{listing_score[0]}.{listing_score[1]}"
			
			rating_checkboxs = [self.scrapper.find_element(By.ID, "ReviewRatingFilter_5"),
							self.scrapper.find_element(By.ID, "ReviewRatingFilter_4"),
							self.scrapper.find_element(By.ID, "ReviewRatingFilter_2"),
							self.scrapper.find_element(By.ID, "ReviewRatingFilter_1")]

			for rating_checkbox in rating_checkboxs:
				print("click on rating box")
				self.scrapper.execute_script("arguments[0].click()",rating_checkbox)
				sleep(1)
				
				for num_page in range(1, num_pages+1):
					print(f"scraping page number {num_page}")
					# get reviews cards
					reviews_els = self.scrapper.find_elements(By.CSS_SELECTOR, "div[data-test-target='HR_CC_CARD']")
					# get data of each review
					for review in reviews_els:
						# get opinion holder
						review_holder = review.find_element(By.CSS_SELECTOR, ".ui_header_link").text

						# get rating
						rating = review.find_element(By.CSS_SELECTOR, "div[data-test-target='review-rating'] span")
						rating = rating.get_attribute("class")[-2:]
						review_rating = rating[0] + "." + rating[1]

						# get review title
						review_title = review.find_element(By.CSS_SELECTOR, "div[data-test-target='review-title']")
						review_title_str = review_title.text
						# click to show the rest of comment
						read_more = review.find_element(By.CSS_SELECTOR, 'div[data-test-target="expand-review"]')
						self.scrapper.execute_script("arguments[0].click()", read_more)

						# get review
						review_str = review.find_element(By.CSS_SELECTOR, "div._T q._a").text
						reviews.append({
							'listing_name': listing_name, 'listing_score': listing_score, 'username': review_holder,
							'review_score': review_rating, 'review_title': review_title_str, 'review': review_str
						})
					
					# break pages for loop if the there is no next page for this rating
					if not self.go_to_next_page():
						break
				self.scrapper.execute_script("arguments[0].click()", rating_checkbox)
				print("===================")
				sleep(1)
		except Exception as e:
			print(e)

		return reviews

	def go_to_next_page(self) -> bool:
		# go to the next page
		try:
			self.scrapper.implicitly_wait(0.5)
			self.scrapper.find_element(By.CSS_SELECTOR, "a.next").click()
			self.scrapper.implicitly_wait(10)
			sleep(1)
			return True
		except NoSuchElementException as e:
			print("no next page avalibale for this rating")
			self.scrapper.implicitly_wait(10)
			return False
