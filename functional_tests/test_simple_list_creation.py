from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # user_1 has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy a friggin napkin'" into a text box (user_1's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy a friggin napkin')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy a friggin napkin'" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy a friggin napkin')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to Wipe yer bloody nose wit it" (user_1 is very
        # methodical)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to Wipe yer bloody nose wit it')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('2: Use peacock feathers to Wipe yer bloody nose wit it')
        self.wait_for_row_in_list_table('1: Buy a friggin napkin')

        # Satisfied, she goes back to sleep


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # user_1 start a new todo list
        self.browser.get(self.server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy a friggin napkin')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy a friggin napkin')

        # She notices that her list has a unique URL
        user_1_list_url = self.browser.current_url
        self.assertRegex(user_1_list_url, '/lists/.+')

        # Now a new user, user_2, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of user_1's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # user_2 visits the home page.  There is no sign of user_1's
        # list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a friggin napkin', page_text)
        self.assertNotIn('Wipe yer bloody nose wit it', page_text)

        # user_2 starts a new list by entering a new item. He
        # is less interesting than user_1...
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Dont do a damn thing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Dont do a damn thing')

        # user_2 gets his own unique URL
        user_2_list_url = self.browser.current_url
        self.assertRegex(user_2_list_url, '/lists/.+')
        self.assertNotEqual(user_2_list_url, user_1_list_url)

        # Again, there is no trace of user_1's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a friggin napkin', page_text)
        self.assertIn('Dont do a damn thing', page_text)

        # Satisfied, they both go back to sleep