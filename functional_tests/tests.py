from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time


class NewVisitorTest(LiveServerTestCase):
	def setUp(self) -> None:
		self.browser = webdriver.Firefox(
			executable_path='C:\\Users\\jakub\\OneDrive\\Documents\\Python Scripts\\TDD\\geckodriver.exe')

	def tearDown(self) -> None:
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id("id_list_table")
		rows = table.find_elements_by_tag_name("tr")
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
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
		time.sleep(1)

		self.check_for_row_in_list_table("1: Buy a friggin napkin")
		# The text box remains available to insert other items
		# User inserts another item in the TO-DO list
		inputbox = self.browser.find_element_by_id("id_new_item")
		inputbox.send_keys("Use the friggin napkin to wipe yer' bloody nose")
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		# Page updates again, now showing two items in the list
		self.check_for_row_in_list_table("1: Buy a friggin napkin")
		self.check_for_row_in_list_table("2: Use the friggin napkin to wipe yer' bloody nose")
		# User wonders if the list is persistent. Sees that the site has generated unique URL for him
		self.fail("Proceed with the tests!")
		# there is and explanation text to that effect

		# User tries the url to find his list still there

		# Satisfied user leaves for the moment
