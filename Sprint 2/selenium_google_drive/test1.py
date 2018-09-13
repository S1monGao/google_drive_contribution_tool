from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_style import get_colour_from_text_style
import time


def get_users_and_colours(revision):
    """
    Creates an array of user/colour tuples
    :param revision: A revision element in the drive HTML
    :return: An array of tuples in the form ("User's name, e.g. John Smith", "Colour of user's icon as a tuple, e.g. (0, 255, 62)")
    """
    users = []

    #Get HTML element containing list of users
    user_list = revision.find_element_by_xpath('.//div[@class="docs-revisions-tile-collaborator-list"]')

    #Get each user's element
    user_divs = user_list.find_elements_by_xpath('.//div[@class="docs-revisions-tile-collaborator-name"]')

    for user_div in user_divs:
        user_name = user_div.text

        #Find the symbol of the user
        user_symbol = user_div.find_element_by_xpath('.//div[@class="docs-revisions-tile-swatch"]')
        user_colour = user_symbol.get_attribute('style')
        users.append((user_name, get_colour_from_text_style(user_colour)))
    return users


# Create a webdriver for scraping
driver = webdriver.Chrome()

test_doc_address = "https://docs.google.com/document/d/1M0wxSlTC2x_2xep7VE2IbId2vOaz3D4hwX04Hcup29c/edit"
unit_test_doc_address = 'https://docs.google.com/document/d/1TyFzFJ5F3e3JL9uFXr8pB58uGEMFlreZoqxNrR0V7NA/edit'

#Open unit_Test_Doc
driver.get(test_doc_address)

#It will ask you to login. You have 13 secs to do this, otherwise program will not work (to be fixed later)
time.sleep(13)

#Press CTRL-ALT-SHIFT-H to open version history
ActionChains(driver)\
    .key_down(Keys.CONTROL) \
    .key_down(Keys.ALT) \
    .key_down(Keys.SHIFT) \
    .send_keys('h') \
    .perform()

#Un-press
ActionChains(driver)\
    .key_up(Keys.CONTROL) \
    .key_up(Keys.ALT) \
    .key_up(Keys.SHIFT) \
    .perform()

#Sleep again to make sure it has time to load version history
time.sleep(3)



#Find revisions from side bar
all_revisions_on_page = driver.find_elements_by_xpath('//div[@class="docs-revisions-collapsible-pane-milestone-tile-container"]')

for revision in all_revisions_on_page:
    #click on revision
    revision.click()
    #Give time for content to load
    time.sleep(3)

    pages = driver.find_elements_by_xpath('//div[contains(@class, "kix-page-content-wrapper")]')

    # The first half of pages are not pages that we want. Only the second half is needed (not really sure why)
    first_page_index = len(pages) // 2
    pages = pages[first_page_index:]

    for i in range(len(pages)):
        page = pages[i]

        # We have to go to each page and stay there for the DOM to load to get all the content on the page
        time.sleep(3)
        ActionChains(driver).move_to_element(page).perform()

        # Get all the lines on the page
        all_items = page.find_elements_by_xpath('.//span[contains(@class, "kix-wordhtmlgenerator-word-node")]')

        for item in all_items:
            if len(item.text.strip()) > 0:
                print(item.text)

                # Find the rgb of the text
                print(get_colour_from_text_style(item.get_attribute('style')))
        print("************")
    print(get_users_and_colours(revision))
    print("----------------")

"""
Current Issues:
 - Main problem: can only see changes on first page
 - Secondary problem: colour in right column for user is slightly different to colour used in text
 - Also haven't looked into checking for the strike-through to differentiate addition and deletion
"""

