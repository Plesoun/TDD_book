from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):
	def setUp(self) -> None:
		self.browser = webdriver.Firefox(
			executable_path='C:\\Users\\jakub\\OneDrive\\Documents\\Python Scripts\\TDD\\geckodriver.exe')

	def tearDown(self) -> None:
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# User checks frontpage
		self.browser.get("http://localhost:8000")

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

		table = self.browser.find_element_by_id("id_list_table")
		rows = table.find_elements_by_tag_name("tr")
		self.assertTrue(
			any(row.text == "1: Buy a friggin napkin" for row in rows),
			"A new item did not appear in the table"
		)
		# The text box remains available to insert other items
		self.fail("Proceed with the tests!")
	# User inserts another item in the TO-DO list

	# Page updates again, now showing two items in the list

	# User wonders if the list is persistent. Sees that the site has generated unique URL for him
	# there is and explanation text to that effect

	# User tries the url to find his list still there

	# Satisfied user leaves for the moment


if __name__ == "__main__":
	unittest.main()
