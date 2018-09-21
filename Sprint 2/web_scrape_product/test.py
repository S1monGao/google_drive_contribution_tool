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


#class TestDocs(unittest.TestCase):

    


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
    testGraphs()
    #unittest.main()
