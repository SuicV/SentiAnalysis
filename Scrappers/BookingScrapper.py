import configparser
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class BookingScrapper:
	"""
	class to scrap data from Booking.com
	"""
	def __init__(self):
		"""
		constructor method used to initialize chrome driver and class parameters
		:param output reviews output file
		"""
		config_parser = configparser.ConfigParser()
		config_parser.read(".env")
		chrome_options = Options()
		# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
		# chrome_options.add_argument("--disable-extensions")
		# chrome_options.add_argument("--disable-gpu")
		# chrome_options.add_argument("--headless")
		self.scrapper = webdriver.Chrome(config_parser["SELENIUM"]["DRIVER_PATH"], options=chrome_options)
		self.scrapper.implicitly_wait(10)
    
	def get_hotels(self, search_tag):
		"""
		method to get list of hotels by a search tag.
		Example "Paris Hotels" will return a list of hotels in Paris
		
		:param search_tag: query to search in tripadvisor landing page form

		:return dataframe contains the following columns {'listing_name', 'listing_score', 'link'} or
			False if there is an Exception
		"""
		links = []
		try:
			self.scrapper.get("https://booking.com")
			# get search field
			search_input = self.scrapper.find_element(By.CSS_SELECTOR, "#ss")
			# type search tag in the field
			search_input.send_keys(search_tag)
			# click on search button
			self.scrapper.find_element(By.CSS_SELECTOR, "button.sb-searchbox__button ").click()
			sleep(1.5)
			# get results
			review_cards = self.scrapper.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")
			for review_card in review_cards:
				listing_link = review_card.find_element(By.CSS_SELECTOR, 'a[data-testid="title-link"]').get_dom_attribute("href")
				listing_title = review_card.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text
				listing_score = float(review_card.find_element(By.CSS_SELECTOR, "div[aria-label^='Scored']").text)/2
				links.append({"listing_name": listing_title, "listing_score":listing_score, "link": listing_link})
		except Exception as e:
			print(e)
			return False
		return links

	def get_reviews(self, link, num_pages=1):
		"""
		method to get reviews of a hotel by it's link.

		:param link the link of hotel
		:param num_pages maximal pages of reviews to scrap
		"""
		reviews = []
		try:
			self.scrapper.get(f"{link}")
			# get hotel name
			listing_name = self.scrapper.find_element(By.CSS_SELECTOR, "#hp_hotel_name").text
			# show reviews by clicking on geust reviews button
			self.scrapper.find_element(By.CSS_SELECTOR, "#show_reviews_tab").click()
			sleep(1.5)
			# get hotel score
			listing_score = float(self.scrapper.find_element(By.CSS_SELECTOR, ".reviews_panel_header_score .review-score-badge").text)
			print(listing_name, listing_score)
			# filter reviews by english language
			self.scrapper.find_element(By.CSS_SELECTOR, "#review_lang_filter button").click()
			self.scrapper.find_element(By.CSS_SELECTOR, "#review_lang_filter button[data-value='en']").click()
			sleep(2)

			for num_page in range(1, num_pages+1):
				print(f"scraping page {num_page}")
				
				# parse all reviews in review list to get review data
				list_reviews = self.scrapper.find_elements(By.CSS_SELECTOR, ".review_list > li")
				for review_section in list_reviews:
					# get review metadata
					review_holder = review_section.find_element(By.CSS_SELECTOR, "span.bui-avatar-block__title").text
					review_score = review_section.find_element(By.CSS_SELECTOR, ".bui-review-score__badge").text
					review_score = float(review_score)/2 if review_score != "" else review_score
					review_title = review_section.find_element(By.CSS_SELECTOR, ".c-review-block__title").text
					review_rows = review_section.find_elements(By.CSS_SELECTOR, ".c-review__body")
					# join positive and negative blocs by dot (.)
					review_text = ".".join([i.text for i in review_rows])
					
					# ignore review
					if review_text == "There are no comments available for this review":
						continue

					reviews.append({
						"username": review_holder, "review_score": review_score, "review_title": review_title, "review": review_text
					})
					print(review_holder, review_title, review_score,"\n", review_text)
					print("=====================")
				# break for loop pages when there isn't next page
				if not self.next_page():
					break

		except Exception as e_:
			print(e_)

		return reviews

	def next_page(self):
		try:
			self.scrapper.implicitly_wait(0.5)
			# click on the next page link if it's availabe, if not it will throw NoSuchElementException
			self.scrapper.find_element(By.CSS_SELECTOR, "a.pagenext").click()
			self.scrapper.implicitly_wait(10)
			# wait for new page to load into dom
			sleep(2)
			return True
		except NoSuchElementException as e:
			print("no next page available")
			self.scrapper.implicitly_wait(10)
			return False
		