import configparser
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class AgodaScrapper:
	"""
	class to scrap data from Agoda.com
	"""
	def __init__(self):
		"""
		constructor method used to initialize chrome driver and class parameters
		:param output reviews output file
		"""
		config_parser = configparser.ConfigParser()
		config_parser.read(".env")
		chrome_options = Options()
		chrome_options.add_argument('--disable-blink-features=AutomationControlled')
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument("--disable-gpu")
		chrome_options.add_argument("--start-maximized")
		chrome_options.add_argument("--headless")
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
		# open landing page, which contains the search form
		self.scrapper.get("https://www.agoda.com")
		
		close_ad_modal = self.scrapper.find_element(By.CSS_SELECTOR, 'button[class="ab-close-button"][aria-label="Close Message"]')
		close_ad_modal.click()
		# type the search tag into search field
		input_field = self.scrapper.find_element(By.CSS_SELECTOR, 'input[data-selenium="textInput"]')
		input_field.send_keys(search_tag)
		input_field.send_keys(Keys.ENTER)
		sleep(3)
		self.scrapper.save_screenshot("1.png")
		# close search modal
		self.scrapper.execute_script("document.body.click()")
		
		# click on search button
		search_button = self.scrapper.find_element(By.CSS_SELECTOR, "button[data-selenium='searchButton']")
		self.scrapper.execute_script("arguments[0].click()", search_button)
		# scroll to bottom page to load more data
		sleep(5)
		hotels_list = self.scrapper.find_elements(By.CSS_SELECTOR, "li[data-selenium='hotel-item']")

		self.scrapper.execute_script("window.scrollTo(0, document.body.offsetHeight)")
		sleep(5)
		self.scrapper.implicitly_wait(1)
		for hotel_item in hotels_list:
			# get hotels metadata
			# sometimes selenium can't find elements, for that i fill the values with empty string
			try:
				hotel_name = hotel_item.find_element(By.CSS_SELECTOR, 'h3[data-selenium="hotel-name"]').text
			except NoSuchElementException:
				hotel_name = ""
				pass
			try:
				hotel_score = hotel_item.find_element(By.CSS_SELECTOR, "div[data-element-name='property-card-review'] p").text
			except NoSuchElementException:
				hotel_score = ""
				pass
			try:
				hotel_link = f'https://www.agoda.com{hotel_item.find_element(By.CSS_SELECTOR, "a.PropertyCard__Link").get_dom_attribute("href")}'
			except NoSuchElementException:
				continue

			links.append({"listing_name": hotel_name, "listing_score": hotel_score, "link": hotel_link})
			
		self.scrapper.implicitly_wait(10)
		print(len(links))
		return links

	def get_reviews(self, link, num_pages=1):
		"""
		scraps reviews from hotel link. this method goes through pages and scrap reviews at each page. 

		:param link hotel link
		:param num_pages maximum number of pages to scrap

		:return links array of dicts {"listing_name", "listing_score", "username", "review_score", "review_title", "review"}
		"""
		reviews = []
		try:
			# open hotel link
			self.scrapper.get(f"{link}")
			# get hotel name
			listing_name = self.scrapper.find_element(By.CSS_SELECTOR, 'h1[data-selenium="hotel-header-name"]').text
			# get hotel score
			listing_score = self.scrapper.find_element(By.CSS_SELECTOR, 'div[data-selenium="hotel-header-review-rating"] h3').text
			# close check-in date pop-up
			self.scrapper.execute_script("document.body.click()")
			sleep(0.5)
			# scroll to reivew section
			review_button = self.scrapper.find_element(By.CSS_SELECTOR, 'li[data-element-name="customer-reviews-panel-navbar-menu"]')
			self.scrapper.execute_script("arguments[0].click()", review_button)
			sleep(1)
			# filter by language to get English reviews only
			language_dropdown = self.scrapper.find_element(By.CSS_SELECTOR, 'div[data-selenium="reviews-language-filter"]')
			self.scrapper.execute_script("arguments[0].click()", language_dropdown)
			for language in language_dropdown.find_elements(By.TAG_NAME, "li"):
				if language.text == "English":
					self.scrapper.execute_script("arguments[0].click()", language)
					break
			for num_page in range(1, num_pages + 1):
				# get reivews list
				print(f"scanning page {num_page}")
				list_reviews = self.scrapper.find_elements(By.CSS_SELECTOR, "div[id^='review-']")
				for review_section in list_reviews:
					# get metadata
					review_holder = review_section.find_element(By.CSS_SELECTOR, "div.Review-comment-reviewer strong").text
					review_score = review_section.find_element(By.CSS_SELECTOR, "div.Review-comment-leftScore").text
					review_title = review_section.find_element(By.CSS_SELECTOR, "p.Review-comment-bodyTitle").text
					review_text_els = review_section.find_elements(By.CSS_SELECTOR, "p.Review-comment-bodyText")
					# sometimes text review will be splited inside many p tags, for that add the for loop to merge them in one 
					review_text = ""
					for review_text_el in review_text_els:
						review_text += f" {review_text_el.text}."
					review_text = review_text.strip()
					print(review_holder, review_score, review_title)
					reviews.append({
						"listing_name": listing_name,
						"listing_score": listing_score,
						"username": review_holder,
						"review_score": review_score,
						"review_title": review_title,
						"review": review_text
					})
				if not self.next_page():
					break
		except Exception as e_:
			print(e_.__cause__)
			print(e_)

		return reviews

	def next_page(self):
		try:
			# change implicitly_wait because the button is instantly available, no need to wait
			self.scrapper.implicitly_wait(0.5)
			# click on the next page link if it's availabe, if not it will throw NoSuchElementException
			next_page_narrow = self.scrapper.find_element(By.CSS_SELECTOR, "div.Review-paginator-steps .ficon-carrouselarrow-right")
			self.scrapper.implicitly_wait(10)
			# if the parent has inactive in class value, then there isn't a next page
			if "inactive" in next_page_narrow.find_element(By.XPATH, "./..").get_dom_attribute("class"):
				return False
			# click on next page narrow
			self.scrapper.execute_script("arguments[0].click()", next_page_narrow)			
			# wait for new page to load into dom
			sleep(2.5)
			return True
		except NoSuchElementException as e:
			print("no next page available")
			self.scrapper.implicitly_wait(10)
			return False
