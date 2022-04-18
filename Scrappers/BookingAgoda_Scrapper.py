from Scrappers.AgodaScrapper import AgodaScrapper
from time import sleep

from selenium.webdriver.common.by import By


class BookingAgoda_Scrapper(AgodaScrapper):
	"""
	class to scrap booking reivews from agoda platform
	"""
	def __init__(self):
		super().__init__()
		pass

	def get_reviews(self, link: str, num_pages=1) -> list:
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
			# click on booking reviews
			for el in self.scrapper.find_elements(By.CSS_SELECTOR, 'span[data-element-name="review-tab"]'):
				if "booking.com" in el.text.lower():
					self.scrapper.execute_script("arguments[0].click()", el)
					break
			sleep(0.9)
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
					review_title = review_section.find_element(By.CSS_SELECTOR, "p.Review-comment-bodyTitle").text[:-1].strip()
					review_text_els = review_section.find_elements(By.CSS_SELECTOR, ".Review-comment-bodyText")
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
