"""
Algorithm for differentiating between deletions and additions

dec_widths = [] # An array of decorations (strikethroughs that denote a deletion) for a paragraph in the form (width, colour), e.g. (10.00, (100,0,255))
contents = [] # An array of sections from a paragraph in the form (width, colour, content), e.g. (100.00 (100,0,255), "Test content")

deletions = [] # Stores all contents that correpsond to deletions
additions = [] # Same for additions

for content in contents:
    deletion_found = False
    for dec_width in dec_widths:
        if abs(dec_widths[0] - content[0]) < 1 and dec_width[1] == content[1]: # We can match a decoration with the content if they have similar length and same colour
            deletions.append(content)
            deletion_found = True
        if deletion_found:
            dec_widths.remove(dec_width)
            break
    if not deletion_found:
        additions.append(content)

"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
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


def get_decorations_and_contents(paragraph):
    """
    Find all strike-throughs and text sections of a paragraph (really a line)
    :param paragraph: paragraph element from DOM
    :return: 2 arrays: one for all the decoration (strike-through) elements in the pargraph, one for all the text elements
    """
    decoration_elements = paragraph.find_elements_by_xpath('.//div[@class="kix-lineview-decorations"]')
    decoration_elements = [element.find_element_by_xpath('.//div') for element in decoration_elements]
    content_elements = paragraph.find_elements_by_xpath('.//span[@class="kix-wordhtmlgenerator-word-node"]')
    return decoration_elements, content_elements


def get_length_from_decoration_element(element):
    """
    Gets the width of a given strike-through from its corresponding DOM element
    :param element: A decoration DOM element
    :return: The length of the strike-through as stated in the style attribute of the element in pixels
    """
    style = element.get_attribute('style')
    style = style.split(";")
    i = 0
    while "width" not in style[i]:
        i += 1
    return style[i].split(":")[1][:-2]


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
        all_paragraphs = page.find_elements_by_xpath('.//div[contains(@class, "kix-paragraphrenderer")]')
        print(len(all_paragraphs))
        for paragraph in all_paragraphs:
            decoration_elements, content_elements = get_decorations_and_contents(paragraph)
            if len(content_elements) > 0:
                print(content_elements[0].size)
            else:
                print("Text has no content")
            if len(decoration_elements) > 0:
                print(get_length_from_decoration_element(decoration_elements[0]))
            else:
                print("Text has no decoration")

        print("************")
    print(get_users_and_colours(revision))
    print("----------------")

"""
Current Issues:
 - Secondary problem: colour in right column for user is slightly different to colour used in text
 - Working on checking for the strike-through to differentiate addition and deletion
"""



