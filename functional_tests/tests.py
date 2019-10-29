from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
	def setUp(self) -> None:
		self.browser = webdriver.Firefox(
			executable_path='C:\\Users\\jakub\\OneDrive\\Documents\\Python Scripts\\TDD\\geckodriver.exe')

	def tearDown(self) -> None:
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id("id_list_table")
				rows = table.find_elements_by_tag_name("tr")
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_can_start_a_list_for_one_user(self):
		# User checks frontpage
		self.browser.get(self.live_server_url)

		# User notices various features on the front page
		self.assertIn('To-Do', self.browser.title)

		# User notices the TO-DO title
		self.assertIn("To-Do", self.browser.title)
		header_text = self.browser.find_element_by_tag_name("h1").text
		self.assertIn("To-Do", header_text)

		# User notices the text box
		inputbox = self.browser.find_element_by_id("id_new_item")
		self.assertEqual(
			inputbox.get_attribute("placeholder"),
			"Enter a to-do item"
		)

		# User enters items for your TO-DO list into an available text box
		inputbox.send_keys("Buy a friggin napkin")

		# Upon hitting enter, page updates and lists the added item as a TO-DO list item
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy a friggin napkin")

		# The text box remains available to insert other items
		# User inserts another item in the TO-DO list
		inputbox = self.browser.find_element_by_id("id_new_item")
		inputbox.send_keys("Use the friggin napkin to wipe yer' bloody nose")
		inputbox.send_keys(Keys.ENTER)

		# Page updates again, now showing two items in the list
		self.wait_for_row_in_list_table("1: Buy a friggin napkin")
		self.wait_for_row_in_list_table("2: Use the friggin napkin to wipe yer' bloody nose")
		# Satisfied user leaves for the moment

	def test_multiple_users_can_start_lists_at_different_urls(self):
		# User starts a new TO-DO list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id("id_new_item")
		inputbox.send_keys("Buy a friggin napkin")
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy a friggin napkin")

		user_list_url = self.browser.current_url
		self.assertRegex(user_list_url, "/lists/.+")

		# New user comes along to the site

		## We use new browser session
		self.browser.quit()
		self.browser.webdriver.Firefox(
			executable_path='C:\\Users\\jakub\\OneDrive\\Documents\\Python Scripts\\TDD\\geckodriver.exe')

		# New User visits homepage, there is no sign of previous user's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name("body").text
		self.assertNotIn("Buy a friggin napkin", page_text)
		self.assertNotIn("yer' bloody nose", page_text)

		# New User starts a new list by entering a new item
		inputbox = self.browser.find_element_by_id("id_new_item")
		inputbox.send_keys("Get rekt")
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Get rekt")
		# New User gets his own url
		new_user_list_url = self.browser.current_url
		self.assertRegex(new_user_list_url, "/lists/.+")
		self.assertNotEqual(new_user_list_url, user_list_url)

		# There needs to be no trace of other user's list
		page_text = self.browser.find_element_by_tag_name("body").text
		self.assertNotIn("Buy a friggin napkin", page_text)
		self.assertIn("Get rekt", page_text)

		# Users go away
		self.fail("Proceed with the tests!")
