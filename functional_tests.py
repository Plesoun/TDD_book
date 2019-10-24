from selenium import webdriver
import unittest


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
		self.fail("Finish the test")
	# User notices the TO-DO title

	# User enters items for your TO-DO list into an available text box

	# Upon hitting enter, page updates and lists the added item as a TO-DO list item

	# The text box remains available to insert other items

	# User inserts another item in the TO-DO list

	# Page updates again, now showing two items in the list

	# User wonders if the list is persistent. Sees that the site has generated unique URL for him
	# there is and explanation text to that effect

	# User tries the url to find his list still there

	# Satisfied user leaves for the moment


if __name__ == "__main__":
	unittest.main()
