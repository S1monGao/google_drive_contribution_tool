
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime as dt
import matplotlib.pyplot as plt
from classes import User_v2, Revision
import unittest
import weShowedUp


class TestDocs(unittest.TestCase):

    def test_Names(self):
        #Tests to see if functions can find names of everyone who edited a file
        service = weShowedUp.authenticate()
        files = weShowedUp.getDocsNSheets(service)

        file = weShowedUp.getFileInfo('unit_Test_Doc', files)
        revisions = weShowedUp.getRevisions(file, service)
        users = weShowedUp.handleRevisionData(revisions, service)
        #unit_Test_Doc was edited by Josh then Keith then Glyn
        self.assertEqual(len(users),3)
        self.assertEqual(users[0].name, 'Josh De')
        self.assertEqual(users[1].name, 'Keith Pang')
        self.assertEqual(users[2].name, 'Glyn Kendall')
        #this is currently not being passed because our code combines everyones contributions to josh and does not record the other editors


    def test_Contribution(self):
        #tests to see if program can find the additions and deletions of each user
        service = weShowedUp.authenticate()
        files = weShowedUp.getDocsNSheets(service)

        file = weShowedUp.getFileInfo('unit_Test_Doc', files)
        revisions = weShowedUp.getRevisions(file, service)
        users = weShowedUp.handleRevisionData(revisions, service)
        #Josh added 20 and deleted 10, keith added 10 and glyn added 10
        self.assertEqual(users[0].num_added, 20)
        self.assertEqual(users[0].num_deleted, 10)
        self.assertEqual(users[1].num_added, 10)
        self.assertEqual(users[2].num_added, 10)
        #This is not currently passed as the program states josh added 30 and deleted none and no one else edited the file


def testGraphs():
    #tests the graphs using fake users
    users=[0,0,0,0]
    users[0] = User_v2('Josh')
    users[0].add_revision(Revision(60, dt.datetime(2018, 9, 6, 11, 54, 0), True))
    users[0].add_revision(Revision(10, dt.datetime(2018, 9, 6, 11, 59, 0), False))

    users[1] = User_v2('Keith')
    users[1].add_revision(Revision(50, dt.datetime(2018, 9, 5, 11, 54, 0), True))
    users[1].add_revision(Revision(25, dt.datetime(2018, 9, 7, 11, 59, 0), False))

    users[2] = User_v2('Glyn')
    users[2].add_revision(Revision(40, dt.datetime(2018, 10, 5, 11, 54, 0), True))
    users[2].add_revision(Revision(40, dt.datetime(2018, 10, 7, 11, 59, 0), False))

    users[3] = User_v2('Michael')
    users[3].add_revision(Revision(25, dt.datetime(2018, 10, 13, 11, 59, 0), False))

    #shows pie graph where all users have positive total revisions, piegraph is as expected and passes test
    weShowedUp.plot_pie_chart(users[0:3])

    #shows graph where one editor has more deletions than aditions
    #its not possible to have a pie graph with negative proportion so the display is wonky
    #in the next sprint we are seperating pie graph into 2: 1 for additions and 1 for deletions
    weShowedUp.plot_pie_chart(users)

    #plots the adition and deletion line graphs, these are as expected and pass the test
    weShowedUp.plot_lines(users, dt.datetime(2018, 9, 4, 11, 54, 0), dt.datetime(2018, 10, 14, 11, 59, 0), True)
    weShowedUp.plot_lines(users, dt.datetime(2018, 9, 4, 11, 54, 0), dt.datetime(2018, 10, 14, 11, 59, 0), False)



if __name__ == '__main__':
    testGraphs()
    unittest.main()
