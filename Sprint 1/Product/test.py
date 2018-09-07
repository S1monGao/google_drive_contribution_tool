
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
    '''
    def test_Names(self):
        service = weShowedUp.authenticate()
        files = weShowedUp.getDocsNSheets(service)

        file = weShowedUp.getFileInfo('unit_Test_Doc', files)
        revisions = weShowedUp.getRevisions(file, service)
        users = weShowedUp.handleRevisionData(revisions, service)

        self.assertEqual(len(users),3)
        self.assertEqual(users[0].name, 'Josh De')
        self.assertEqual(users[1].name, 'Keith Pang')
        self.assertEqual(users[2].name, 'Glyn Kendall')
    '''
    def test_Contribution(self):
        service = weShowedUp.authenticate()
        files = weShowedUp.getDocsNSheets(service)

        file = weShowedUp.getFileInfo('unit_Test_Doc', files)
        revisions = weShowedUp.getRevisions(file, service)
        users = weShowedUp.handleRevisionData(revisions, service)

        self.assertEqual(users[0].num_added, 20)
        self.assertEqual(users[0].num_deleted, 10)
        self.assertEqual(users[1].num_added, 10)
        self.assertEqual(users[2].num_added, 10)



def testGraphs():
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


    weShowedUp.plot_pie_chart(users[0:3])
    weShowedUp.plot_pie_chart(users)

    weShowedUp.plot_lines(users, dt.datetime(2018, 9, 4, 11, 54, 0), dt.datetime(2018, 10, 14, 11, 59, 0), True)
    weShowedUp.plot_lines(users, dt.datetime(2018, 9, 4, 11, 54, 0), dt.datetime(2018, 10, 14, 11, 59, 0), False)



if __name__ == '__main__':
    # testGraphs()
    unittest.main()
