from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ast import literal_eval
from classes import User, Edit
from plotting_functions import plot_pie_chart, plot_lines, save_all_plots
import time
import datetime as dt
import platform
from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import main_file
import unittest


def testContributions():
    # Create dictionary to convert from colour of edit to colour of user
    edit_colours = [(121, 85, 72), (0, 121, 107), (198, 69, 0), (81, 45, 168), (194, 24, 91), (6, 116, 179),
                    (69, 90, 100)]
    user_colours = [(93, 64, 55), (38, 166, 154), (245, 124, 0), (103, 58, 183), (216, 27, 96), (3, 169, 244),
                    (84, 110, 122)]
    edit_colour_to_user_colour = dict(zip(edit_colours, user_colours))

    current_year = "2018"

    # Asks user for start andend time
    start_time = dt.datetime.strptime('1/9/2018', '%d/%m/%Y')
    end_time = dt.datetime.strptime('1/10/2018', '%d/%m/%Y')

    # Ensures that the user specified times are valid
    while start_time > end_time:
        print("Invalid Dates detected\n Please enter a start time before the end time\n")
        start_time = dt.datetime.strptime(input("Enter a start time in Date/Time format: ie 4/7/2016: "),
                                          '%d/%m/%Y')
        end_time = dt.datetime.strptime(input("Enter an end time in Date/Time format: ir 4/7/2016: "), '%d/%m/%Y')

    # username = input("Enter user_name: ")
    # password = input("Enter password: ")

    # Create a webdriver for scraping
    driver = webdriver.Chrome()

    test_doc_address = "https://docs.google.com/document/d/1M0wxSlTC2x_2xep7VE2IbId2vOaz3D4hwX04Hcup29c/edit"
    unit_test_doc_address = 'https://docs.google.com/document/d/1TyFzFJ5F3e3JL9uFXr8pB58uGEMFlreZoqxNrR0V7NA/edit'

    # Open unit_Test_Doc
    driver.get(unit_test_doc_address)

    """
    # Input and enter username
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(username)
    driver.find_element_by_xpath("//div[@id='identifierNext']").click()

    # Wait for password input element to be visible (presence doesnt seem to work here)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(password)

    # Input and enter password
    # driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
    driver.find_element_by_xpath("//div[@id='passwordNext']").click()
    """

    # Ensures Google Docs loads first
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//div[@role='tablist']")))

    if platform.system() == "Darwin":
        # Press COMMAND-ALT-SHIFT-H to open version history
        ActionChains(driver) \
            .key_down(Keys.COMMAND) \
            .key_down(Keys.ALT) \
            .key_down(Keys.SHIFT) \
            .send_keys('h') \
            .perform()

        # Un-press
        ActionChains(driver) \
            .key_up(Keys.COMMAND) \
            .key_up(Keys.ALT) \
            .key_up(Keys.SHIFT) \
            .perform()
    else:
        # Press CTRL-ALT-SHIFT-H to open version history
        ActionChains(driver) \
            .key_down(Keys.CONTROL) \
            .key_down(Keys.ALT) \
            .key_down(Keys.SHIFT) \
            .send_keys('h') \
            .perform()

        ActionChains(driver) \
            .key_up(Keys.CONTROL) \
            .key_up(Keys.ALT) \
            .key_up(Keys.SHIFT) \
            .perform()

    # Will store all User class instances
    users = []

    # Sleep again to make sure it has time to load version history
    time.sleep(3)

    # Find revisions from side bar
    all_revisions_on_page = driver.find_elements_by_xpath(
        '//div[@class="docs-revisions-collapsible-pane-milestone-tile-container"]')

    for revision in all_revisions_on_page:
        # click on revision
        revision.click()
        # Give time for content to load
        time.sleep(3)

        pages = driver.find_elements_by_xpath('//div[contains(@class, "kix-page-content-wrapper")]')
        revision_datetime_string = revision.find_element_by_xpath(
            './/textarea[contains(@class, "docs-revisions-tile-text-box")]').text
        doc_date_string = revision_datetime_string
        num_commas = doc_date_string.count(",")
        if num_commas == 1:
            index_first_comma = doc_date_string.index(",")
            doc_date_string = doc_date_string[:index_first_comma + 1] + " " + current_year + "," + doc_date_string[
                                                                                                   index_first_comma + 1:]
            revision_datetime = dt.datetime.strptime(doc_date_string, '%B %d, %Y, %I:%M %p')



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
                decoration_elements, content_elements = main_file.get_decorations_and_contents(paragraph)
                processed_decorations = [main_file.process_decoration_element(element) for element in decoration_elements]
                processed_contents = [main_file.process_content_element(element) for element in content_elements]
                paragraph_additions, paragraph_deletions = main_file.get_paragraph_additions_and_deletions(
                    processed_decorations, processed_contents)
                all_additions += paragraph_additions
                all_deletions += paragraph_deletions

        user_tuples = main_file.get_users_and_colours(revision)

        # Adding new User class instances to users array if needed

        # Every user tuple is in the form (name_string, colour_3_tuple)
        for user_tuple in user_tuples:
            user_found = False
            for user_instance in users:
                # Compare by colour not name as users may have same name
                if user_tuple[1] == user_instance.colour:
                    user_found = True
            if not user_found:
                users.append(User(user_tuple[0], user_tuple[1]))

        # Adding additions/deletions to each User class instance

        # Every addition/deletion is in the form (width, colour_3_tuple, content_string)
        for addition in all_additions:
            edit = Edit(revision_datetime, addition[2], True)
            converted_colour = edit_colour_to_user_colour[addition[1]]
            for user in users:
                if user.colour == converted_colour:
                    user.add_edit(edit)
                    break

        for deletion in all_deletions:
            edit = Edit(revision_datetime, deletion[2], False)
            converted_colour = edit_colour_to_user_colour[deletion[1]]
            for user in users:
                if user.colour == converted_colour:
                    user.add_edit(edit)
                    break



    driver.close()

    total_added = sum(user.num_added for user in users)
    total_deleted = sum(user.num_deleted for user in users)

    for user in users:
        print("Name: {0}".format(user.name))
        print("Num_added: {0}".format(str(user.num_added)))
        print("Num_deleted: {0}".format(str(user.num_deleted)))
        for edit in user.edits:
            print("Change: ",edit.content," Time: ",edit.time," Addition: ",edit.is_add,"   Num of char: ",edit.num_chars)
        print("*************")




def testGraphs():
    #tests the graphs using fake users
    users=[0,0,0,0]
    users[0] = User('Josh',(255,0,0))
    users[0].add_edit(Edit(dt.datetime(2018, 9, 6, 11, 59, 0), '1', False))
    users[0].add_edit(Edit(dt.datetime(2018, 9, 6, 11, 54, 0),'123456', True))

    users[1] = User('Keith',(0,255,0))
    users[1].add_edit(Edit(dt.datetime(2018, 9, 7, 11, 59, 0), '123', False))
    users[1].add_edit(Edit(dt.datetime(2018, 9, 5, 11, 54, 0),'12345', True))


    users[2] = User('Glyn',(0,0,255))
    users[2].add_edit(Edit(dt.datetime(2018, 10, 7, 11, 59, 0), '1234', False))
    users[2].add_edit(Edit(dt.datetime(2018, 10, 5, 11, 54, 0),'1234', True))


    users[3] = User('Michael',(100,100,100))
    users[3].add_edit(Edit(dt.datetime(2018, 10, 13, 11, 59, 0),'45', False))



    plt1 = main_file.plot_pie_chart(users,True)
    plt2 = main_file.plot_pie_chart(users,False)
    plt3 = main_file.plot_lines(users, dt.datetime(2018, 9, 4, 11, 54, 0), dt.datetime(2018, 10, 14, 11, 59, 0), True)
    plt4 = main_file.plot_lines(users, dt.datetime(2018, 9, 4, 11, 54, 0), dt.datetime(2018, 10, 14, 11, 59, 0), False)

    save_all_plots([plt1,plt2,plt3,plt4],'testGraphs.pdf')

if __name__ == '__main__':
    #testGraphs()
    testContributions()

    #The obtaining and storing changees from the drive for google docs and graphs and all asosiated fetures have been checked manually by the team and approved by QA as done to the D.O.D.