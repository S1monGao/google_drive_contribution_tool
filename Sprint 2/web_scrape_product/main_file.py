from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from ast import literal_eval
from classes import User, Edit
import time
import datetime as dt


def get_paragraph_additions_and_deletions(dec_widths, contents):
    """

    :param dec_widths: An array of decorations (strikethroughs that denote a deletion) for a paragraph in the form (width, colour), e.g. (10.00, (100,0,255))
    :param contents: An array of sections from a paragraph in the form (width, colour, content), e.g. (100.00 (100,0,255), "Test content")
    :return: an array of additions and deletions from a paragraphs
    """
    deletions = []  # Stores all contents that correpsond to deletions
    additions = []  # Same for additions

    for content in contents:
        if content[1] != (0, 0, 0) and len(content[2].strip()) > 0:  # Not part of an edit
            deletion_found = False
            for dec_width in dec_widths:
                if 0.9 < dec_width[0]/content[0] < 1.1 and dec_width[1] == content[1]:  # We can match a decoration with the content if they have similar length and same colour
                    deletions.append(content)
                    deletion_found = True
                if deletion_found:
                    dec_widths.remove(dec_width)
                    break
            if not deletion_found:
                additions.append(content)
    return additions, deletions


def get_colour_from_text_style(style_string):
    """
    Converts the style attribute of an HTML element into a tuple of 3 rgb numbers
    :param style_string: The style attribute of the element
    :return: An rgb tuple, e.g. (0, 255, 62)
    """

    # Remove spaces and split by ";"
    style_string = style_string.replace(" ", "").split(";")

    # Search for colour section
    i = 0
    while "rgb" not in style_string[i]:
        i += 1
    colour_section = style_string[i]

    #Isolate tuple
    colour = colour_section.split(":")[1]
    colour_tuple = colour[3:]

    # Convert string that looks like a tuple to a tuple
    return literal_eval(colour_tuple)


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


def process_decoration_element(element):
    """
    Gets the width of a given strike-through from its corresponding DOM element
    :param element: A decoration DOM element
    :return: The length of the strike-through as stated in the style attribute of the element in pixels
    """
    style = element.get_attribute('style')
    style = style.split(";")
    i = 0 # index for width
    j = 0 # index for colour
    while "width" not in style[i]:
        i += 1
    while j < len(style) and "rgb" not in style[j]:
        j += 1
    length = style[i].split(":")[1][:-2]
    colour = "000000"
    if j < len(style):
        colour = style[j].split('rgb')[1]
    return (float(length), literal_eval(colour))


def process_content_element(element):
    """
    Converts the style attribute of an HTML element into a tuple of 3 rgb numbers
    :param style_string: The style attribute of the element
    :return: An rgb tuple, e.g. (0, 255, 62)
    """

    # Remove spaces and split by ";"
    content = element.text
    style_string = element.get_attribute('style')
    colour_tuple = get_colour_from_text_style(style_string)
    length = element.size['width']
    return (length, colour_tuple, content)


# Create dictionary to convert from colour of edit to colour of user
edit_colours = [(121, 85, 72), (0, 121, 107), (198, 69, 0), (85, 45, 168), (194, 24, 91), (6, 116, 179), (69, 90, 100)]
user_colours = [(93, 64, 55), (38, 166, 154), (245, 124,0), (103, 58, 183), (216, 27, 96), (3, 169, 244), (84, 110, 122)]
edit_colour_to_user_colour = dict(zip(edit_colours, user_colours))


def convert_doc_date_to_datetime(doc_date_string):
    """
    Converts datetime string from Google Docs HTML to datetime object
    :param doc_date_string: String of date and time of revision from Google Docs
    :return: A datetime object representing this date and time
    """

    # If revision happened in current year, no year will be shown and doc_date_string will only have one comma
    num_commas = doc_date_string.count(",")
    if num_commas == 1:
        index_first_comma = doc_date_string.index(",")
        doc_date_string = doc_date_string[:index_first_comma + 1] + " " + current_year + "," + doc_date_string[index_first_comma + 1:]
    return dt.datetime.strptime(doc_date_string, '%B %d, %Y, %I:%M %p')


current_year = "2018"



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

users = []

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

    all_additions = []
    all_deletions = []

    for i in range(len(pages)):
        page = pages[i]

        # We have to go to each page and stay there for the DOM to load to get all the content on the page
        time.sleep(3)
        ActionChains(driver).move_to_element(page).perform()

        # Get all the lines on the page
        all_paragraphs = page.find_elements_by_xpath('.//div[contains(@class, "kix-paragraphrenderer")]')

        for paragraph in all_paragraphs:
            decoration_elements, content_elements = get_decorations_and_contents(paragraph)
            processed_decorations = [process_decoration_element(element) for element in decoration_elements]
            processed_contents = [process_content_element(element) for element in content_elements]
            paragraph_additions, paragraph_deletions = get_paragraph_additions_and_deletions(processed_decorations, processed_contents)
            all_additions += paragraph_additions
            all_deletions += paragraph_deletions
    print(all_additions)
    print(all_deletions)
    print(get_users_and_colours(revision))
    print("----------------")

driver.close()

"""
Current Issues:
 - Secondary problem: colour in right column for user is slightly different to colour used in text
"""



